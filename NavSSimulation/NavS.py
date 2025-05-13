import numpy as np
import matplotlib.pyplot as plt

#Based vague on: https://nbviewer.org/github/barbagroup/CFDPython/blob/master/lessons/15_Step_12.ipynb


nx = 41
ny = 41

nt = 100

widthOfChannel = 6

dx = widthOfChannel/(nx-1)
dy = widthOfChannel/(ny-1)

x = np.linspace(0,widthOfChannel,nx)
y = np.linspace(0,widthOfChannel,ny)

X,Y = np.meshgrid(x,y)

rho = 1
mu = 0.1
P = -1
dt = .05

u = np.zeros((ny,nx))
v = np.zeros((ny,nx))

def newu(u,nx,ny,dt,dx,dy,rho,P,mu):
    un = u.copy()
    for i in range(1,nx-1):
        for j in range(1,ny-1):
            un[i,j] = u[i,j] + (dt/rho)*(-P+mu*((u[i+1,j]+u[i-1,j]+2*u[i,j])/dx**2 + (u[i,j+1]+u[i,j-1]+2*u[i,j])/dy**2))

    un[0,:]=0
    un[-1,:]=0

    return un

def newv(v,nx,ny,dt,dx,dy,rho,mu):
    vn = v.copy()
    for i in range(1,nx-1):
        for j in range(1,ny-1):
            vn[i,j] = v[i,j] + (dt*mu/rho)*((v[i+1,j]+v[i-1,j]+2*v[i,j])/dx**2 + (v[i,j+1]+v[i,j-1]+2*v[i,j])/dy**2)

    vn[0,:]=0
    vn[-1,:]=0

    return vn

def run(u,v,nx,ny,dt,dx,dy,rho,P,mu):
    un = u.copy()
    vn = v.copy()
    for n in range(nt):
        un = newu(un,nx,ny,dt,dx,dy,rho,P,mu)
        vn = newv(vn,nx,ny,dt,dx,dy,rho,mu)
    return un,vn

un,vn = run(u,v,nx,ny,dt,dx,dy,rho,P,mu)

plt.plot(y,un[:,int(nx/2)], label='CFD') # 
plt.ylabel('u-velocity')
plt.xlabel('y')
plt.legend()
plt.show()