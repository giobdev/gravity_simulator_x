import turtle, random, sys
from time_manager import TimeStep
from bodies.planet import *
from bodies.star import *
from bodies.satellite import *
from physics_manager import PhysicsManager
from trajectory import Trajectory
from camera_manager import Camera
import tkinter as tk
from tkinter import messagebox
#from database import *

#seed fighi
#4487033921494198826
#3686757135635109634
#6796014375224988179
#4467910743155316225 SUPER TOP
class Main():
	def __init__(self):
		self.win = turtle.Screen()
		self.win.tracer(False)
		self.win.title("Gravity Simulator X")
		self.win.setup(1200, 800)

		turtle.speed(speed="fastest")

		self.lastSeed = random.randrange(sys.maxsize)
	
	def showcase_system(self):
		self.bodies = [Planet(1, -600, 0, 0, -2000), 
				 Planet(1, 600, 0, 0, 2000), 
				 Planet(1, 0, -600, 2000, 0), 
				 Planet(1, -0, 600, -2000, 0),
				 Satellite(1, 589, 0, 0 , 1200),
				 Satellite(1, -589, 0, 0 , -1200),
				 Satellite(0.6, -611, 8, 0 , -1200),
				 Star(0.5, 0, 0, 0, 0)]
	
	def random_system_generator(self, n_planets: int = 6, n_stars: int = 2, n_satellites: int = 25):
		# PLANETS
		self.bodies = [Planet(self.rng.uniform(0.5, 1.5), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-2300, 2300),  
						self.rng.randint(-2300, 2300)) for _ in range(1, n_planets)]

		# SATELLITES
		self.bodies +=[Satellite(self.rng.uniform(0.5, 1.5), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-2300, 2300),  
						self.rng.randint(-2300, 2300), 10**10) for _ in range(1, n_satellites)]
		
		# STARS
		self.bodies +=[Star(self.rng.uniform(0.3, 0.8), 
						0, 
						0, 
						0,  
						0) for _ in range(1, n_stars)]
	
	def restartWithLastSeed(self):
		self.restart(self.lastSeed)

	def restart(self, seed=4467910743155316225):
		print("restart")
		self.timeStep = TimeStep()
		self.timeStep.setTempo("2x")
		if seed is None:
			seed = random.randrange(sys.maxsize)
		else:
			self.timeStep.setTempo("2x")
		self.lastSeed = seed
		self.rng = random.Random(seed)
		print(seed)

		self.win.clear()
		self.win.bgcolor("black")
		self.win.tracer(0)
		self.win.onkeypress(self.restart, "space")
		self.win.onkeypress(self.restartWithLastSeed, "r")
		self.win.onkeypress(self.timeStep.rewind, "b")
		self.win.onkeypress(self.timeStep.forward, "f")
		self.win.onkeypress(self.timeStep.fastForward, "h")
		self.win.listen()

		self.showcase_system()
		#self.random_system_generator()
		
		self.physicsManager = PhysicsManager(self.bodies, self.timeStep)
		self.trajectory = Trajectory(self.bodies, self.timeStep)

		#salva il try nel db
		#try_id = insert_try(seed)
		#if try_id:
		#	for body in self.bodies:
		#		if isinstance(body, Planet):  #solo i pianite vengono registrati
		#			insert_planet(try_id, body)

		self.camera = Camera()

		for body in self.bodies:
			body.draw()
		
		for body in self.trajectory.bodies:
			body.draw()
			body.drawTrajectory()

	def mainLoop(self):
		self.win.update()
		TO_FOLLOW = -1

		for _ in range(int(self.timeStep.getTempo())):
			self.timeStep.nextStep()
			self.camera.recenter(TO_FOLLOW, self.bodies)
			self.physicsManager.applyAllForces()

			for body in self.bodies:
				try:
					body.draw()
				except:
					pass

				body.updateAll(self.timeStep.getStepTime())

		for i in range(int(self.timeStep.getTempo() * 2)):
			self.camera.recenter(TO_FOLLOW, self.trajectory.bodies)
			self.trajectory.physicsManager.applyAllForces()

			for body in self.trajectory.bodies:
				if i <= 1:
					if body.body_name != "star" and body.body_name != "satellite":
						if self.timeStep.elapsed_time < 0.58:
							body.drawTrajectory()
				body.updateAll(self.timeStep.getAbsStepTime())
	
		if window_active: self.win.ontimer(self.mainLoop, 10) 

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
		#connect_to_database()
		app.restart()
		app.mainLoop()
		app.win.mainloop()

	except turtle.Terminator:
		pass
	#Finally viene sempre eseguito, indipendentemente dal fatto che si verifichino errori
	finally:
		#Resetta lo stato della finestra, consentendo l'avvio di una nuova simulazione casuale (diversa dalla precedente)
		#print("Finestra chiusa")
		window_active = False
		
		
		try:
			turtle.bye()
		except turtle.Terminator:
			pass
		#print("Nessuna finestra da chiudere.")


#if __name__ == "__main__":
#	app = Main()
#	connect_to_database()  # Connessione al database
#	app.restart()
#	app.mainLoop()

#	app.win.mainloop()
