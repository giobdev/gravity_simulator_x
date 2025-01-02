import turtle
from time_manager import TimeStep
from bodies.planet import *
from bodies.star import *
from bodies.satellite import *
from physics_manager import PhysicsManager
from bodies.common import Body


#Creazione di un'istanza di TimeStep, cioè viene creato un oggetto usando la classe TimeStep
#time_step = TimeStep() 
#Lista globale dei corpi



def start_simulation(bodies):

	print(f"I corpi inseriti sono:{len(bodies)}")

	#Crea la finestra Turtle
	win = turtle.Screen()
	win.title("Celestial Simulator X")
	win.setup(1200, 800)
	win.bgcolor("black")
	win.tracer(0)

	print("Turtle window created.")

	#Inizializza la simulazione
	timeStep = TimeStep()
	physicsManager = PhysicsManager(bodies)

	try:
		while True:
			win.update()
			timeStep.nextStep()
			physicsManager.applyAllForces()
			for body in bodies:
				body.updateAll(timeStep.getStepTime(), timeStep.getTempo())
				body.draw()
	except turtle.Terminator:
		print("Turtle window closed.")
	
	

def reset_simulation(bodies):
	bodies.clear()

	global window_active
	
	print(f"i corpi inseriti sono {bodies}")
	print("Resetting simulation...")

	#Ciclo che chiude la finestra Turtle
	try:
		turtle.bye()
		print("Turtle window closed.")
	except turtle.Terminator:
		print("Turtle window was already closed.")

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


