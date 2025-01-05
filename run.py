import turtle, random, sys
from time_manager import TimeStep
from bodies.planet import *
from bodies.star import *
from bodies.satellite import *
from physics_manager import PhysicsManager
from trajectory import Trajectory
from camera_manager import Camera
from database import *

#Inizializzazioni
#gestore fisica
#physiscsManager = PhysicsManager(bodies)


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
		self.clip_log = []

		self.user_input = ""

		turtle.speed(speed="fastest")

		self.lastSeed = random.randrange(sys.maxsize)


		connect_to_database()
	
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

		#aggiungere bottoni per rewind, restartWithLastSeed, forward e fastForward
		self.win.clear()
		self.win.bgcolor("black")
		self.win.tracer(0)
		self.win.onkeypress(self.restart, "space")
		self.win.onkeypress(self.restartWithLastSeed, "r")
		self.win.onkeypress(self.timeStep.rewind, "b")
		self.win.onkeypress(self.timeStep.forward, "f")
		self.win.onkeypress(self.timeStep.fastForward, "h")
		#l'utente inseriesce le cifre (caratteri numerici) con i tasti da 0 a 9
		for c in "0123456789":
			self.win.onkey(lambda d=c: self.inserimento(d), c)
		self.win.onkey(lambda: self.inserimento("BackSpace"), "BackSpace")
		self.win.onkey(lambda: self.inserimento("Return"), "Return")
		self.win.onkey(lambda: exit(), "q")  
		self.win.listen()
		self.win.onscreenclick(onClick)
		self.win.listen()

		self.showcase_system()
		#self.random_system_generator()
		
		self.physicsManager = PhysicsManager(self.bodies, self.timeStep)
		self.trajectory = Trajectory(self.bodies, self.timeStep)

		#salva il try nel db
		try_id = insert_try(seed)
		if try_id:
			for body in self.bodies:
				if isinstance(body, Planet):  #solo i pianite vengono registrati
					self.insert_planet(try_id, body)

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
				body.draw()
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
	
		self.win.ontimer(self.mainLoop, 10)
	
	#ok
	def salva_clip(self):
		self.centratura = 1.0
		clip = self.timeStep.creaClip(self.bodies, self.centratura)
		self.clip_log.append(clip)
		print(f"Clip salvata: {clip}")
	
	#new
		clip_id = self.insert_clip(clip['time_step'], clip['planet_count'], clip['planet_ids'], clip['planet_coords'])
		if clip_id:
			print(f"Clip salvata nel db con ID: {clip_id}")

	#ok
	def insert_clip(self, time_step, planet_count, planet_ids, planet_coords):
		if db_connection is None:
			print("Connessione al db non disponibile.")
			return None
		try:
			cursor = db_connection.cursor()
			query = """ INSERT INTO clips (time_step, planet_count, planet_ids, planet_coords)
			VALUES (%s, %s, %s, %s)"""

			cursor.execute(query(time_step, planet_count, str(planet_ids), str(planet_coords)))
			db_connection.commit()

			cursor.execute("SELECT LAST_INSERT_ID();")
			clip_id = cursor.fetchone()[0]
			return clip_id
		except Error as e:
			print(f"Errore dirante l'inserimentod ella clip: {e}")
			return None

	#ok
	#rewindToTime
	def rewindToT(self):
		#leggo l'input dell'utente
		if self.user_input.isdigit():
			time_step = int(self.user_input)
			clip = self.timeStep.rewindTo(time_step)

			if clip:
				print(f"Il sistema è tornato a {clip['time_step']} con stabilità {clip['stabilita']}.")
				self.reset_sistema()
			else:
				print("Nessuna clip disponibile per il tempo specificato")	
		else:
			print("Valore inserito non valido, riprovare.")

	#ok
	def reset_sistema(self):
		for body in self.bodies:
			body.clear()
		self.timeStep.reset()	


	def insert_planet(self, clip_id, planet):
		query = """
    	INSERT INTO planets (clip_id, name, mass, x_coord, y_coord) 
    	VALUES (%s, %s, %s, %s, %s);
    	"""
		cursor.execute(query, (clip_id, planet.name, planet.mass, planet.x, planet.y))
		connection.commit()

	def connect_to_database(self):
		"""Metodo per connettersi al database (supponendo l'uso di MySQL)"""
		global connection, cursor
		connection = pymysql.connect(host='localhost', user='root', password='password', database='gravity_simulator')
		cursor = connection.cursor()

	def close_database(self):
		"""Chiude la connessione al database"""
		cursor.close()
		connection.close()

	def inserimento(self, key):
		#cancella
		if key == "BackSpace":
			self.user_input = self.user_input[:-1]
		#invio -> non succede nulla
		elif key == "Return":
			return
		#inserimento cifra
		elif key.isdigit():
			self.user_input += key
		self.upd_input(casella_input, self.user_input)

	def upd_input(self, input_box, text):
		input_box.clear() #resetto il contenuto della casella
		input_box.write(
			text,
			align="left",
			font=("Arial", 14, "normal")
		)


def onClick(mouse_x, mouse_y):
		for button in buttons:
			if button["x"] <= mouse_x <= button["x"] + button["w"] and button["y"] <= mouse_y <= button["y"] + button["h"]:
				print(mouse_x)
				button["callback"]()


buttons = []

#Per creare un bottone cliccabile
#argomenti: x,y -> posizione del bottone; w, h -> dimensioni; text -> testo; callback -> funzione eseguita al click del bottone
def create_button(x, y, w, h, text, callback):
	button = turtle.Turtle()
	button.hideturtle()
	button.penup()
	button.goto(x, y)
	button.pendown()
	button.color("white", "gray")
	button.begin_fill()
	for i in range(2):
		button.forward(w)
		button.left(90)
		button.forward(h)
		button.left(90)
	button.end_fill()

	#testo bottone
	button.penup()
	button.goto(x + w / 2, y + h / 2 - 10)  
	button.color("white")
	button.write(text, align="center", font=("Arial", 14, "bold"))
	buttons.append({"x": x, "y": y, "w": w, "h": h, "callback": callback})
#Per creare un bottone cliccabile
#argomenti: x,y -> posizione del bottone; w, h -> dimensioni; text -> testo; callback -> funzione eseguita al click del bottone

#casella x input utente
def create_input_box(x, y, w, h):
    input_box = turtle.Turtle()
    input_box.hideturtle()
    input_box.penup()
    input_box.goto(x, y)
    input_box.pendown()
    input_box.color("white", "black")
    input_box.begin_fill()
    input_box.forward(w) #larghezza
    input_box.left(90)
    input_box.forward(h) #altezza
    input_box.left(90)
    input_box.forward(w)
    input_box.left(90)
    input_box.forward(h)
    input_box.left(90)
    input_box.end_fill()

    input_box.penup()
    input_box.goto(x + 5, y + h - 25) #posizione testo nel bottone
    return input_box


if __name__ == "__main__":
	app = Main()
	app.restart()
	#app.mainLoop()
	#Bottone salvaClip
	create_button(-550, 300, 100, 40, "Salva clip", app.salva_clip)
	#Bottone rewindTo
	create_button(-550, 350, 100, 40, "Torna a", app.rewindToT)
	#casella x input
	casella_input = create_input_box(-430, 350, 100, 40)
	app.mainLoop()
	connect_to_database()  # Connessione al database
	app.win.mainloop()