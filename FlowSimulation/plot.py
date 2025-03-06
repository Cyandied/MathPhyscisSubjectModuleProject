import matplotlib.pyplot as mat
import pandas as pd

db = pd.read_csv("output\HydrodynamicProfile.dat",delimiter=" ")

print(db)
print(db.columns)

mat.plot(db["pos_z"],db["velocity"])
