#!/usr/bin/python3

#PBS -W umask=002
import os

if "PBS_O_WORKDIR" in os.environ:
    os.chdir(os.environ["PBS_O_WORKDIR"])

print("hello world!")

import random as r

print("Generating a random integer between 1 and 10...")

print(r.randint(1,10))

print("Wasn't that awesome!?")

print("I will now solve this math 2/3 * 7 * 9/13 + 90")

print(f'2/3 * 7 * 9/13 + 90 = {2/3 * 7 * 9/13 + 90}')

print("Hell yeah!")

print("I'll now raise a cool exception :)")

raise Exception("B)")
