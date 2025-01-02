import mysql.connector
from mysql.connector import Error

db_connection = 0

def connect_to_database():
	global db_connection
	try:
		db_connection = mysql.connector.connect(
			host='localhost',  
			user='root',  
			password='',  
			database='gravity_simulator'
		)
		print("Connesso al database!")
	except Error as e:
		print(f"Errore nella connessione al database: {e}")
		db_connection = None

def insert_try(seed):
	try:
		if db_connection is None:
			print("Connessione al database non disponibile.")
			return None

		cursor = db_connection.cursor()
		query = "INSERT INTO tries (seed) VALUES (%s)"
		cursor.execute(query, (seed,))
		db_connection.commit()
		print(f"Tentativo registrato con ID: {cursor.lastrowid}")
		return cursor.lastrowid
	except Error as e:
		print(f"Errore durante l'inserimento del tentativo: {e}")
		return None

def insert_planet(try_id, planet):
	try:
		if db_connection is None:
			print("Connessione al database non disponibile.")
			return

		cursor = db_connection.cursor()
		query = """
			INSERT INTO planets (try_id, mass, x, y, vx, vy)
			VALUES (%s, %s, %s, %s, %s, %s)
		"""
		values = (try_id, planet.mass, planet.x, planet.y, planet.speed_x, planet.speed_y)
		cursor.execute(query, values)
		db_connection.commit()
		print(f"Pianeta registrato con ID: {cursor.lastrowid}")
	except Error as e:
		print(f"Errore durante l'inserimento del pianeta: {e}")
