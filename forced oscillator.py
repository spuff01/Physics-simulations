import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, axs = plt.subplots(2, 1)

k = 4
m = 1
v = [0]
dt = 0.01
a = [0]
t=[0]
b=0.3
omega = 5
F0 = 10
x= [ F0 / np.sqrt((k - m*omega**2)**2 + (b*omega)**2)]
E=[0.5*k*x[0]**2]
K=[0]
P=[0.5*k*x[0]**2]


def animate(i):
    a.append(((F0*np.sin(omega*t[-1]))-k*x[-1]-b*v[-1])/m)
    v.append(v[-1]+a[-1]*dt)
    x.append(x[-1]+v[-1]*dt)
    t.append(t[-1]+dt)
    E.append(0.5*m*v[-1]**2+0.5*k*x[-1]**2)
    K.append(0.5*m*v[-1]**2)
    P.append(0.5*k*x[-1]**2)
    axs[0].cla()
    axs[1].cla()

    axs[0].plot(t, E, label  ='E')
    axs[0].plot(t, K, label = 'K.E')
    axs[0].plot(t, P, label = 'P.E')
    axs[0].set_xlabel('Time(t)')
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(t, x, label='x')
    axs[1].plot(t, v, label='v')
    axs[1].plot(t,a, label = 'a')
    axs[1].set_xlabel('Time(t)')
    axs[1].legend()
    axs[1].grid(True)

ani = FuncAnimation(fig, animate, interval = 100, cache_frame_data=False)
plt.tight_layout()
plt.show()















