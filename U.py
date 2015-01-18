
from matplotlib import *
import matplotlib.pyplot as plt
import numpy as np
import time

from matplotlib.ticker import EngFormatter

plt.ion()

numIndividuos = 100
calidad = [0]*numIndividuos

for i in range(numIndividuos-1):
	calidad[i+1] = calidad[i] + 1

fig = plt.figure()

fig.suptitle('Calidades', fontsize=15)


ax = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
# ax.set_xscale('log')
# formatter = EngFormatter(unit='Hz', places=1)
# ax.xaxis.set_major_formatter(formatter)

for i in range(100):
	ax.clear()
	ax.grid(True)
	inds = [(j) for j in range(i+1)]
	ax.plot(inds[:i], calidad[:i])
	plt.draw()
	time.sleep(0.025)

for i in range(100):
	ax2.clear()
	ax2.grid(True)
	inds = [(j) for j in range(i+1)]
	ax2.plot(inds[:i], calidad[:i])
	plt.draw()
	time.sleep(0.025)

plt.show('all')