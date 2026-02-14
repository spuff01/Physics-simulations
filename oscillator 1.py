import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()

k = 4
m = 1
x= [1]
v = [0]
dt = 0.1
a = [0]
t=[0]
E=[0.5*k*x[0]**2]
K=[0]
P=[0.5*k*x[0]**2]
c=0.3


def animate(i):
    a.append(-k*x[-1]-c*v[-1])
    v.append(v[-1]+a[-1]*dt)
    x.append(x[-1]+v[-1]*dt)
    t.append(t[-1]+dt)
    E.append(0.5*m*v[-1]**2+0.5*k*x[-1]**2)
    K.append(0.5*m*v[-1]**2)
    P.append(0.5*k*x[-1]**2)
    ax.cla()

    ax.plot(t, E, label  ='E')
    ax.plot(t, K, label = 'K.E')
    ax.plot(t, P, label = 'P.E')
    ax.set_xlabel('Time(t)')
    ax.legend()
    ax.grid(True)

ani = FuncAnimation(fig, animate, interval = 10, cache_frame_data=False)
plt.tight_layout()
plt.show()















