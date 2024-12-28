import turtle
from time_manager import TimeStep
from physics_manager import PhysicsManager
from run import Main

# Creazione di un'istanza di TimeStep, cioè viene creato un oggetto usando la classe TimeStep
time_step = TimeStep() 
bodies = []


#Funzione per impostare la velocità della simulazione
def set_simulation_speed(scale):
    speed = scale.get()
    time_step.setTempo(f"{speed}x")
    #Maggiore è speed dato dall'utente, più velocemente procede la simulazione (step)
    time_step.step = 0.01 / speed

def random():
    app = Main(bodies)
    app.restart()
    app.mainLoop()

def start_simulation(bodies):
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