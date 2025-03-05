#!/usr/bin/python3

#PBS -W umask=002
import os

if "PBS_O_WORKDIR" in os.environ:
    os.chdir(os.environ["PBS_O_WORKDIR"])

import rumdpy as rp
import numpy as np
# import matplotlib.pyplot as plt

#Lattice structure
configuration = rp.Configuration(3)


configuration.make_lattice(
    rp.unit_cells.FCC,
    [8,8,8],
    0.973
)

#Masses and initial velocity
configuration["m"] = 1

temperature = 0.8
configuration.randomize_velocities(temperature)

#Pair potential
pairRaw = rp.LJ_12_6_sigma_epsilon
rMin = 2**(1/6)
uMin, fMin, curvatureMin = pairRaw(rMin,(1,1,np.inf))

pairFunc  =rp.apply_shifted_potential_cutoff(rp.LJ_12_6_sigma_epsilon)

sigma, epsilon, cutoff = 1,1,2.5
pairPot = rp.PairPotential(pairFunc,[sigma, epsilon,cutoff], 1000)

#Integrator
integrator = rp.integrators.NVT(temperature, 0.2,0.005)

#The simulation object
sim = rp.Simulation(
    configuration,
    pairPot,
    integrator,
    [rp.MomentumReset(100),rp.ScalarSaver(16)],
    0,
    10,
    1000,
    storage="output.h5"
)

sim.run()


#Analyze simulation data
U,W,K = rp.extract_scalars(sim.output, ["U","W","K"],1)

dt = sim.dt
time = np.arange(len(U))*dt*16


N = sim.configuration.N

# plt.figure()
# plt.plot(time, U/N)
# plt.xlabel(r'Time, $t$ [$\sigma\sqrt{m/\varepsilon}$]')  # Time in LJ units
# plt.ylabel(r'Potential energy per particle, $U$ [$\varepsilon$]')  # Energy in LJ units
# plt.xlim(0, None)
# plt.show()