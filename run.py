import turtle, random, sys
from time_manager import TimeStep
from bodies.planet import *
from bodies.star import *
from bodies.satellite import *
from physics_manager import PhysicsManager
import tkinter as tk
from tkinter import messagebox


class Main():
	def __init__(self, bodies = None):
		self.win = turtle.Screen()
		self.win.title("Gravity Simulator X")
		self.win.setup(1200, 800)
		self.lastSeed = random.randrange(sys.maxsize)
		
		
	
	def restartWithLastSeed(self):
		self.restart(self.lastSeed)

	def restart(self, seed=None):
		self.timeStep = TimeStep()
		self.timeStep.setTempo("4x")
		if seed is None:
			seed = random.randrange(sys.maxsize)
		else:
			self.timeStep.setTempo("0.2x")
		self.lastSeed = seed
		self.rng = random.Random(seed)
		print(seed)
		self.win.clear()
		self.win.bgcolor("black")
		self.win.tracer(0)
		self.win.onkeypress(self.restart, "space")
		self.win.onkeypress(self.restartWithLastSeed, "r")
		self.win.listen()
		
		"""self.bodies = [Planet(1, -400, 0, 0, -2000), 
				 Planet(1, 400, 0, 0, 2000), 
				 Planet(1, 0, -400, 2000, 0), 
				 Planet(1, -0, 400, -2000, 0), 
				 Star(0.5, 0, 0, 0, 0), 
				 Satellite(4, 390, 0, 0 , 1200),
				 Satellite(4, -380, -350, 380 , 800)]"""
		self.bodies = [Planet(self.rng.uniform(0.5, 1.5), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-2300, 2300),  
						self.rng.randint(-2300, 2300)) for _ in range(0, 15)]
		self.bodies +=[Star(self.rng.uniform(0.5, 1), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-300, 300), 
						0,  
						0) for _ in range(0, 1)]
		self.bodies +=[Satellite(self.rng.uniform(0.5, 1.5), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-2300, 2300),  
						self.rng.randint(-2300, 2300), 10**10) for _ in range(0, 20)]
		self.physicsManager = PhysicsManager(self.bodies)


	def mainLoop(self):
		try:
			while True:
				#RUNNING è una variabile interna di Turtle gestita dalla classe Screen
				#indica se la finestra di Turtle è aperta o chiusa

				#Se la finestra è chiusa, esci dal ciclo while
				if not turtle.Screen()._RUNNING:
					break
				self.win.update()
				self.timeStep.nextStep()
				self.physicsManager.applyAllForces()
				for body in self.bodies:
					self.timeStep.eachTime(3, body.clear)
					body.updateAll(self.timeStep.getStepTime(), self.timeStep.getTempo())
					#timeStep.eachTime(0.1, body.drawTrail)
					body.draw()
		except turtle.Terminator:
			pass


	


# Variabile globale per monitorare lo stato della finestra Turtle
window_active = False


def start_random_simulation():
  
	global window_active

	#Ciclo che controlla se una finestra Turtle è già attiva
	if window_active:
		
		root = tk.Tk()
		root.withdraw()
		messagebox.showerror("Simulation Running", "The simulation window is already active. Please close it to start a new one.")
		root.destroy()
		return

	#Imposta la finestra come attiva
	window_active = True

	#Gestione della finestra Turtle
	try:
		app = Main()
		app.restart()
		app.mainLoop()

	except turtle.Terminator:
		pass
	#Finally viene sempre eseguito, indipendentemente dal fatto che si verifichino errori
	finally:
		#Resetta lo stato della finestra, consentendo l'avvio di una nuova simulazione casuale (diversa dalla precedente)
		#print("Finestra chiusa")
		window_active = False

		#Ciclo che chiude la finestra Turtle per un nuovo avvio
		try:
			turtle.bye()
		except turtle.Terminator:
			pass
			#print("Nessuna finestra da chiudere.")




 
