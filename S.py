import numpy as np
import matplotlib.pyplot as plt

Individuo = [[0.142, 0.213, 0.808, 0.814, 0.705, 0.739, 0.806, 0.997],
[0.186, 0.523, 0.605, 0.745, 0.01, 0.437, 0.722, 0.754],
[0.377, 0.593, 0.67, 0.794, -0.574, -0.08, 0.567, 0.907],
[0.694, 0.781, 0.815, 0.915, 0.092, 0.559, 0.679, 0.787],
[0.011, 0.639, 0.767, 0.97, 0.721, 0.752, 0.845, 0.95]]
t = [0.0, 1.0 ,1.0 , 0.0]

fig = plt.figure()

fig.suptitle('Individuo', fontsize=15)


yprops = dict(rotation=0,
              horizontalalignment='right',
              verticalalignment='center',
              x=-0.01)

axprops = dict(yticks=[])

ax1 = fig.add_subplot(2, 1, 1)
ax1.set_title("Error",fontsize=13)
ax1.plot(Individuo[0][:4], t, label="Muy Izq")
ax1.plot(Individuo[1][:4], t, label="Izq")
ax1.plot(Individuo[2][:4], t, label="Centro")
ax1.plot(Individuo[3][:4], t, label="Der")
ax1.plot(Individuo[4][:4], t, label="Muy Der")
ax1.set_ylabel('S1', **yprops)
ax1.set_yticks([])

ax1.legend(loc='upper left', prop={'size':10})

axprops['sharex'] = ax1
axprops['sharey'] = ax1
# force x axes to remain in register, even with toolbar navigation
ax2 = fig.add_subplot(2, 1, 2)
ax2.set_title("Derivada del Error",fontsize=13)
ax2.plot(Individuo[0][4:8], t)
ax2.plot(Individuo[1][4:8], t)
ax2.plot(Individuo[2][4:8], t)
ax2.plot(Individuo[3][4:8], t)
ax2.plot(Individuo[4][4:8], t)
ax2.set_ylabel('S2', **yprops)
ax2.set_yticks([])


# turn off x ticklabels for all but the lower axes

# setp(ax1.get_xticklabels(), visible=False)

plt.show()