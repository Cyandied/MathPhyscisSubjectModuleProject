#!/usr/bin/python3

#Identifers:

#PBS -m b
#PBS -W umask=002
#PBS -l nodes=1:ppn=1
#PBS -v PYTHONPATH

import random
import os

if "PBS_O_WORKDIR" in os.environ:
    os.chdir(os.environ["PBS_O_WORKDIR"])

import numpy as np
import rumdpy as rp

#Timeblocks and steps
num_timeblocks = 100
steps_per_timeblock = 64

# Some system parameters
nx, ny, nz = 6, 6, 10 #nan, nan, width of channel
rhoWall = 1.0
rhoFluid = 0.7

# Setup a default fcc configuration
configuration = rp.Configuration(D=3)
configuration.make_lattice(rp.unit_cells.FCC, cells=[nx, ny, nz], rho=rhoWall)
configuration['m'] = 1.0


# Fluid particles have type '0', wall particles '1', dummy particles '2'
nwall, npart = 0, configuration.N
hlz = 0.5 * configuration.simbox.lengths[2]
for n in range(npart):
    if configuration['r'][n][2] + hlz < 3.0:
        configuration.ptype[n] = 1
        nwall = nwall + 1

nfluid = np.sum(configuration.ptype == 0)
nfluidWanted = int(nfluid * rhoFluid / rhoWall)

while nfluid > nfluidWanted:
    idx = random.randint(0, npart - 1)
    if configuration.ptype[idx] == 0:
        configuration.ptype[idx] = 2
        nfluid = nfluid - 1

rp.tools.save_configuration(configuration, "initial.xyz")

# Tether specifications. 
tether = rp.Tether()
tether.set_anchor_points_from_types(particle_types=[1], spring_constants=[300.0], configuration=configuration)

# Add gravity force 
grav = rp.Gravity()
grav.set_gravity_from_types(particle_types=[0], forces=[0.01], configuration=configuration)

# Temp relaxation for wall particles
relax = rp.Relaxtemp()
relax.set_relaxation_from_types(particle_types=[1], temperature=[2.],
                                relax_times=[0.01],configuration=configuration); 

# Set the pair interactions
# The siulation is solving newtons euqations, force from potential, for each particle
# This sets paramaters for the potentials
# Differences in pair-potential between fluid-wall and fluid-fluid changes the simulation
pair_func = rp.apply_shifted_potential_cutoff(rp.LJ_12_6_sigma_epsilon)
sig = [[1.0, 1.0, 0.0], [1.0, 1.0, 0.0], [0.0, 0.0, 0.0]] # Controls the minimum
eps = [[1.0, 1.0, 0.0], [1.0, 1.0, 0.0], [0.0, 0.0, 0.0]] # How deep the well is
cut = np.array(sig) * 2.5
pair_pot = rp.PairPotential(pair_func, params=[sig, eps, cut], max_num_nbs=1000)

# Temperature
configuration.randomize_velocities(temperature=2.0)

# Setup integrator: NVT
# Integrators dont actually integrate, they move time forwards
integrator = rp.integrators.NVE(dt=0.005)

# Compute plan
compute_plan = rp.get_default_compute_plan(configuration)

# Setup runtime actions, i.e. actions performed during simulation of timeblocks
runtime_actions = [rp.ConfigurationSaver(), 
                   rp.ScalarSaver()]

# Setup Simulation. Total number of time steps: num_blocks * steps_per_block
sim = rp.Simulation(configuration, [pair_pot, tether, grav, relax], integrator, runtime_actions, 
                    num_timeblocks=num_timeblocks, steps_per_timeblock=steps_per_timeblock,
                    storage='memory', compute_plan=compute_plan)

prof = rp.CalculatorHydrodynamicProfile(configuration, 0)

# Run simulation one block at a time
for block in sim.run_timeblocks():
    print(sim.status(per_particle=True))
    prof.update()

print(sim.summary())

prof.read()

rp.tools.save_configuration(configuration, "final.xyz")

