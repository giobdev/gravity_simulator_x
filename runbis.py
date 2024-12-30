import turtle
from time_manager import TimeStep
from physics_manager import PhysicsManager
from run import Main

# Creazione di un'istanza di TimeStep, cioè viene creato un oggetto usando la classe TimeStep
time_step = TimeStep() 
bodies = []

def start_simulation(bodies):
    print("Hai cliccato start")
    win = turtle.Screen()
    win.title("Celestial Simulator X")
    win.setup(1200, 800)
    win.bgcolor("black")
    win.tracer(0)

    timeStep = TimeStep()
    physicsManager = PhysicsManager(bodies)

    while True:
        win.update()
        timeStep.nextStep()
        physicsManager.applyAllForces()

        for body in bodies:
            body.updateAll(timeStep.getStepTime(), timeStep.getTempo())
            body.draw()