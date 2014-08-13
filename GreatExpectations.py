# robot goes forward and then slows to a stop when it detects something  

import random
import time
import numpy as np
import matplotlib.pyplot as plt

from copy import deepcopy
from datetime import datetime
from pyrobot.brain import Brain

	
class GreatExpectations(Brain):

	numGenes = 8
	global hora;			hora = str(datetime.now().replace(second=0, microsecond=0))
	global fichero;			fichero = open(hora + '--GreatExpectations.txt', 'w')
	global numParticiones;	numParticiones = 5
	global numIndividuos;	numIndividuos = 50
	global numElite;		numElite = 5		# Necesariamente menor que la mitad de numIndividuos
	global maxStp;			maxStp = 200
	global maxGeneraciones;	maxGeneraciones = 50
	global individuo; 		individuo = -1
	global stp;				stp = 0
	global generacion;		generacion = 0
	global error;			error = 0
	global Derror;			Derror = 0
	global luzAlcanzada;	luzAlcanzada = False
	global P;				P = [[[0]*numGenes for i in range(numParticiones)]for j in range(numIndividuos)]
	global FAM;				FAM = [[0]*numGenes for i in range(numParticiones)]	# [part(0..4)][gen(0..7)]
	global tablaSalida;		tablaSalida = [0]*5
	global calidad;			calidad = [0]*numIndividuos
	global calidadMedia;	calidadMedia = [[0]*maxGeneraciones for i in range(2)]

	def setup(self):
		self.robot.light[0].units = "SCALED"
		self.robot.range.units = "ROBOTS"

		self.primeraPoblacion()
		self.generaFAM()


	def step(self):
		global individuo, numIndividuos, generacion, maxGeneraciones, luzAlcanzada, stp

		if (stp != maxStp) and (not luzAlcanzada) and (not self.robot.stall):
			stp += 1
			translation, rotate = self.determineMove()  
			self.robot.move(translation, rotate)

		else:
			self.robot.stop()
			self.asignaCalidad()
			stp = 0
			if individuo == numIndividuos-1:
				self.asignaCalidadGeneracion()
				if generacion == maxGeneraciones-1:
					print("\nTodas las generaciones completadas")
					self.destroy()
				else:
					self.nuevaPoblacion()
			else:
				self.nuevoIndividuo()



	def asignaCalidad(self):
		global individuo, P, elite, calidad, generacion

		if(self.robot.stall):
			calidad[individuo] = -maxStp + stp
		else:
			calidad[individuo] = maxStp - stp
		print("\t\tCalidad " + str(calidad[individuo]))

		if individuo >= numElite:
			for pos in range(numElite):
				if calidad[individuo] > calidad[pos]:
					self.insertaEnElite(pos)
					print("Inserto en pos: " + str(pos) + "Calidades elite: " + str(calidad[:numElite]))
					break
		elif individuo != -1: self.reordenaElite()

	def insertaEnElite(self, pos):
		global numElite, calidad, individuo, P
		auxP = P[:numElite]
		auxC = calidad[:numElite]
		for i in range(pos, numElite-1):
			P[i+1] = deepcopy(auxP[i])
			calidad[i+1] = deepcopy(auxC[i])
		P[pos] = deepcopy(P[individuo])
		calidad[pos] = deepcopy(calidad[individuo])

	def reordenaElite(self):
		global numElite, individuo, calidad, P
		auxP = P[:individuo+1]
		auxC = calidad[:individuo+1]
		auxP, auxC = (list(x) for x in zip(*sorted(zip(auxP, auxC), reverse = True, key=lambda pair: pair[1])))
		P[:individuo+1] = auxP
		calidad[:individuo+1] = auxC


	def nuevoIndividuo(self):
		global individuo, luzAlcanzada, numParticiones, P, error, Derror
		if individuo == numElite-1 and generacion != 0:
			fichero.write("\n\t\tAhora: " + str(calidad[:numElite]))
		individuo += 1
		print("Individuo " + str(individuo)),

		self.engine.robot.simulation[0].setPose(0,0.3,0.3,0)
		error = 0
		Derror = 0
		luzAlcanzada = False


	def primeraPoblacion(self):
		global P, numIndividuos, numParticiones
		for ind in range(numIndividuos): # 0..numIndividuos
			for part in range(numParticiones):		# 0-MI, 1-I, 2-C, 3-D, 4-MD
				# Error: 4 puntos de discontinuidad
				P[ind][part][0] = random.uniform(-1, 0.97)
				P[ind][part][1] = random.uniform(P[ind][part][0], 0.98)
				P[ind][part][2] = random.uniform(P[ind][part][1], 0.99)
				P[ind][part][3] = random.uniform(P[ind][part][2], 1)

				# Derivada del error: 4 puntos de discontinuidad
				P[ind][part][4] = random.uniform(-1, 0.97)
				P[ind][part][5] = random.uniform(P[ind][part][4], 0.98)
				P[ind][part][6] = random.uniform(P[ind][part][5], 0.99)
				P[ind][part][7] = random.uniform(P[ind][part][6], 1)

				for gen in range(0,8):
					P[ind][part][gen] = round(P[ind][part][gen], 3)


	def asignaCalidadGeneracion(self):
		global generacion, numElite, numIndividuos, calidadMedia
		q, qE = 0,0
		for ind in range(numIndividuos):
			q += calidad[ind]
		for indQ in range(numElite):
			qE += calidad[indQ]

		calidadMedia[0][generacion] = qE / numElite			# 0 - Media Elite
		calidadMedia[1][generacion] = q / numIndividuos		# 1 - Media Poblacion

	def nuevaPoblacion(self):
		global P, generacion, individuo, numIndividuos, numElite

		generacion += 1
		individuo = -1

		fichero.write("\n" + str(generacion) + "\tCalidades elite: " + str(calidad[:numElite]))
		print("\nCalidades elite: " + str(calidad[:numElite]))

		print("\nXXXXXXXXXXXXXXXXX Generacion " + str(generacion) + " XXXXXXXXXXXXXXXXX")


		for ind in range(numElite, numIndividuos): # numElite..numIndividuos
			for part in range(0,5):
				for i in range(2):
					if bool(random.getrandbits(1)) == 1:
						self.mutaA(ind, part, i)
						self.mutaB(ind, part, i)
						self.mutaC(ind, part, i)
						self.mutaD(ind, part, i)

				for gen in range(0,8):
					P[ind][part][gen] = round(P[ind][part][gen], 3)

	def mutaA(self, ind, part, i):
		global P
		gen = 0
		if(i==1): gen = 4
		while True:
			rand = random.gauss(0,0.31)
			if (-1 < P[ind][part][gen] + rand <= 0.75):
				P[ind][part][gen] += rand
				break

	def mutaB(self, ind, part, i):
		global P
		gen = 1
		if(i==1): gen = 5
		while True:
			rand = random.gauss(0,0.31)
			if (P[ind][part][gen-1] < P[ind][part][gen] + rand <= 0.80):
				P[ind][part][gen] += rand
				break

	def mutaC(self, ind, part, i):
		global P
		gen = 2
		if(i==1): gen = 6
		while True:
			rand = random.gauss(0,0.31)
			if (P[ind][part][gen-1] < P[ind][part][gen] + rand <= 0.85):
				P[ind][part][gen] += rand
				break

	def mutaD(self, ind, part, i):
		global P
		gen = 3
		if(i==1): gen = 7
		while True:
			rand = random.gauss(0,0.31)
			if (P[ind][part][gen-1] < P[ind][part][gen] + rand <= 1.00):
				P[ind][part][gen] += rand
				break


	def inferencia(self):			#reglas de inferencia
		global individuo, P, tablaSalida, error, Derror

		for particion in range(0,5): # 0, 1, 2, 3, 4

			if P[individuo][particion][0] < error <= P[individuo][particion][3]:
				tablaSalida[particion] = round(self.salida(particion), 3)
			else:
				tablaSalida[particion] = 0


		m = max(tablaSalida)
		maximos = [i for i, j in enumerate(tablaSalida) if j == m]
		return reduce(lambda x, y: x + y, maximos) / len(maximos) # la media de los maximos


	def salida(self, part):
		global FAM, error, Derror, stp

		# ------ Error ------ #

		if FAM[part][0] < error <= FAM[part][1]:
			salidaError = (error - FAM[part][0]) / (FAM[part][1] - FAM[part][0])

		elif FAM[part][1] < error <= FAM[part][2]:
			salidaError = 1

		elif FAM[part][2] < error <= FAM[part][3]:
			salidaError = (FAM[part][3] - error) / (FAM[part][3] - FAM[part][2])

		else:
			salidaError = 0

		# ------ Derror ------ #

		if FAM[part][0] < Derror < FAM[part][1]:
			salidaDerivadaError = (Derror - FAM[part][0]) / (FAM[part][1] - FAM[part][0])

		elif FAM[part][1] < Derror <= FAM[part][2]:
			salidaDerivadaError = 1

		elif FAM[part][2] < Derror <= FAM[part][3]:
			salidaDerivadaError = (FAM[part][3] - Derror) / (FAM[part][3] - FAM[part][2])

		else:
			salidaDerivadaError = 0

		return max(min(salidaError, salidaDerivadaError), 1 - salidaDerivadaError)


	def generaFAM(self):
		global FAM
		FAM[0][0] = -1.0;	FAM[0][1] = -1.0;	FAM[0][2] = -0.75;	FAM[0][3] = -0.5
		FAM[1][0] = -1.0;	FAM[1][1] = -0.75;	FAM[1][2] = -0.25;	FAM[1][3] = 0.0
		FAM[2][0] = -0.5;	FAM[2][1] = -0.25;	FAM[2][2] = 0.25;	FAM[2][3] = 0.5
		FAM[3][0] = 0.0;	FAM[3][1] = 0.25;	FAM[3][2] = 0.75;	FAM[3][3] = 1.0
		FAM[4][0] = 0.5;	FAM[4][1] = 0.75;	FAM[4][2] = 1.0;	FAM[4][3] = 1.0

	def imprimeCALI(self):
		global calidadMedia, maxGeneraciones, hora
		fig2 = plt.figure('Calidades')

		ax3 = fig2.add_subplot(2, 1, 1)
		ax4 = fig2.add_subplot(2, 1, 2)

		ax3 = fig2.add_subplot(2, 1, 1)
		ax3.set_title("Calidad media de la elite",fontsize=13)
		ax3.grid(True)
		ax3.axes.set_ylim(-maxStp,+maxStp)

		ax4 = fig2.add_subplot(2, 1, 2)
		ax4.set_title("Calidad media por generacion",fontsize=13)
		ax4.grid(True)
		ax4.axes.set_ylim(-maxStp,+maxStp)

		ejeX = [0]*maxGeneraciones
		for i in range(maxGeneraciones-1): 
			ejeX[i+1] = ejeX[i] + 1

		ax3.plot(ejeX, calidadMedia[0], label = "media elite")
		ax4.plot(ejeX, calidadMedia[1], label = "media generacion")

		fig2.savefig(hora + '--MediaCalidades')


	def imprimeTOP(self):
		global P, hora
		fig1 = plt.figure('Mejor Individuo')

		fig1.yprops = dict(rotation=0,
					  horizontalalignment='right',
					  verticalalignment='center',
					  x=-0.01)

		fig1.axprops = dict(yticks=[])

		t = [0.0, 1.0 ,1.0 , 0.0]

		ax1 = fig1.add_subplot(2, 1, 1)
		ax1.set_title("Error",fontsize=13)
		ax1.axes.set_xlim(-1,1)
		ax1.set_yticks([0,1])

		ax2 = fig1.add_subplot(2, 1, 2)
		ax2.set_title("Derivada del Error",fontsize=13)
		ax2.axes.set_xlim(-1,1)
		ax2.set_yticks([0,1])

		ax1.plot(P[0][0][:4], t, label="Muy Izq")
		ax1.plot(P[0][1][:4], t, label="Izq")
		ax1.plot(P[0][2][:4], t, label="Centro")
		ax1.plot(P[0][3][:4], t, label="Der")
		ax1.plot(P[0][4][:4], t, label="Muy Der")

		ax1.legend(loc='upper left', prop={'size':10})

		ax2.plot(P[0][0][4:8], t, label="Muy Izq")
		ax2.plot(P[0][1][4:8], t, label="Izq")
		ax2.plot(P[0][2][4:8], t, label="Centro")
		ax2.plot(P[0][3][4:8], t, label="Der")
		ax2.plot(P[0][4][4:8], t, label="Muy Der")

		fig1.savefig(hora + '--MejorIndividuo')


	def determineMove(self):
		global luzAlcanzada, tablaSalida, individuo, error, Derror

		leftLightSensor = self.robot.light[0].value[0]
		rightLightSensor = self.robot.light[0].value[1]
		errorTmenos1 = error
		error = round(rightLightSensor - leftLightSensor, 3)
		Derror = error - errorTmenos1

		if (leftLightSensor > 0.95) or (rightLightSensor > 0.95):
			luzAlcanzada = True

		decision = self.inferencia() # 0..4


		if decision == 0: # Girar Muy Izquierda
			return (0.2, (tablaSalida[decision]*(0.5) + 0.5))
		elif decision == 1: # Girar Izquierda
			return (0.4, tablaSalida[decision]*0.5)
		elif decision == 2: # No girar
			return (0.7, 0.0)
		elif decision == 3: # Girar Derecha
			return (0.4, tablaSalida[decision]*(-0.5))
		else: # Girar Muy Derecha
			return (0.2, (tablaSalida[decision]*(-0.5) - 0.5))


	def destroy(self):
		print("\nFin de simulacion\nFichero cerrado")
		self.imprimeTOP()
		self.imprimeCALI()

		for elite in range(numElite):
			fichero.write("\n\t Elite" + str(elite))
			for part in range(numParticiones):
				fichero.write("\n" + str(P[elite][part]))
		fichero.close()
		self.engine.shutdown()


def INIT(engine):  
	assert (engine.robot.requires("range-sensor") and engine.robot.requires("continuous-movement"))
	brain = GreatExpectations('GreatExpectations', engine)
	print "\nRobot " + engine.robot.name + " cargado con el comportamiento de " + brain.name + "."
	brain.nuevoIndividuo()
	return brain
