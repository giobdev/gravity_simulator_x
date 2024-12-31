import turtle, random, sys
from time_manager import TimeStep
from bodies.planet import *
from bodies.star import *
from bodies.satellite import *
from physics_manager import PhysicsManager
from trajectory import Trajectory

#seed fighi
#4487033921494198826
class Main():
	def __init__(self):
		self.win = turtle.Screen()
		self.win.tracer(0)
		self.win.title("Gravity Simulator X")
		self.win.setup(1200, 800)

		turtle.speed(speed="fastest")

		self.lastSeed = random.randrange(sys.maxsize)
	
	def showcase_system(self):
		self.bodies = [Planet(1, -400, 0, 0, -2000), 
				 Planet(1, 400, 0, 0, 2000), 
				 Planet(1, 0, -400, 2000, 0), 
				 Planet(1, -0, 400, -2000, 0), 
				 Star(0.5, 0, 0, 0, 0)]
				 #Satellite(4, 390, 0, 0 , 1200),
				 #Satellite(4, -380, -350, 380 , 800)]
	
	def random_system_generator(self, n_planets: int = 5, n_stars: int = 1, n_satellites: int = 5):
		# PLANETS
		self.bodies = [Planet(self.rng.uniform(0.5, 1.5), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-2300, 2300),  
						self.rng.randint(-2300, 2300)) for _ in range(0, n_planets)] #range(0, 15)

		# STARS
		self.bodies +=[Star(self.rng.uniform(1.5, 3), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-300, 300), 
						0,  
						0) for _ in range(0, n_stars)]

		# SATELLITES
		"""self.bodies +=[Satellite(self.rng.uniform(0.5, 1.5), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-300, 300), 
						self.rng.randint(-2300, 2300),  
						self.rng.randint(-2300, 2300), 10**10) for _ in range(0, 5)] #range(0, 25)"""
	
	def restartWithLastSeed(self):
		self.restart(self.lastSeed)

	def restart(self, seed=None):
		print("restart")
		self.timeStep = TimeStep()
		self.timeStep.setTempo("4x")
		if seed is None:
			seed = random.randrange(sys.maxsize)
		else:
			self.timeStep.setTempo("1x")
		self.lastSeed = seed
		self.rng = random.Random(seed)
		print(seed)

		self.win.clear()
		self.win.bgcolor("black")
		self.win.tracer(0)
		self.win.onkeypress(self.restart, "space")
		self.win.onkeypress(self.restartWithLastSeed, "r")
		self.win.onkeypress(self.timeStep.rewind, "b")
		self.win.listen()

		self.showcase_system()
		#self.random_system_generator()
		
		self.physicsManager = PhysicsManager(self.bodies, self.timeStep)
		self.trajectory = Trajectory(self.bodies, self.timeStep)

		for body in self.trajectory.bodies:
			body.draw()

	def mainLoop(self):
		#while True:
		self.win.update()

		for _ in range(int(self.timeStep.getTempo())):
			self.timeStep.nextStep()
			self.physicsManager.applyAllForces()

			for body in self.bodies:
				body.updateAll(self.timeStep.getStepTime())
				body.draw()

		for i in range(int(self.timeStep.getTempo() * 2)):
			self.trajectory.physicsManager.applyAllForces()

			for body in self.trajectory.bodies:
				body.updateAll(self.timeStep.getStepTime())
				if i <= 1:
					body.drawTrajectory()
	
		self.win.ontimer(self.mainLoop, 10)

if __name__ == "__main__":
	app = Main()
	app.restart()
	app.mainLoop()
	app.win.mainloop()