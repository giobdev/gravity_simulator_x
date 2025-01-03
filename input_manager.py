import tkinter as tk
from tkinter import messagebox
from bodies.planet import Planet
from bodies.star import Star
from bodies.satellite import Satellite
from run import start_random_simulation
from runbis import start_simulation, reset_simulation
import turtle


#bg (background) = imposta il colore di sfondo di un widget, 
#fg (foreground) = imposta il colore del testo del wid,
#pady aggiunge uno spazione verticale, aumentando la distanza tra il widget e gli altri elementi, sopra o sotto di esso

#Aggiunta di un controllo per limitare posizione e velocità dei corpi inseriti
#simulation_bounds = 400 #realisticamente :1e10 (10miliardi)
#velocity_limit = 200 #100.000

bodies = []

#Variabile globale per la simulazione corrente
#simulation = None


def create_gui():

	#print("Avvio interfaccia grafica...")
	#global simulation
	def start_manual_simulation():
		#Chiudi la finestra principale e passa alla finestra di inserimento corpi
		root.quit()
		root.destroy()
		#Avvia la finestra di inserimento manuale dei corpi celesti
		manual_input_window()

	#Finestra principale
	global root
	root = tk.Tk()
	root.title("Gravity Simulator")
	root.config(bg='black')

	#Imposta una larghezza di 500px e un'altezza di 200px per la finestra principale
	root.geometry("500x200")

	#Disabilita il ridimensionamento della finestra
	root.resizable(False, False)

	# Messaggio visualizzato nella finestra principale
	tk.Label(root, text="Welcome to the Gravity Simulator!", font=("Arial", 16), fg="yellow", bg="black").pack(pady=20)

	# Bottone per la simulazione pre-impostata casuale
	random_button = tk.Button(root, text="Start random simulation", font=("Helvetica", 12), bg="midnight blue", fg="white", command=start_random_simulation)
	random_button.pack(pady=10)

	# Bottone per inserire i corpi manualmente
	manual_button = tk.Button(root, text="Insert bodies manually", font=("Helvetica", 12), bg="midnight blue", fg="white", command=start_manual_simulation)
	manual_button.pack(pady=10)

	root.mainloop()

#Funzione per la finestra di inserimento manuale dei corpi
def manual_input_window():

	def close_manual_window():
		#DistruggE la finestra corrente
		root.destroy()
		#Riapre la finestra principale
		create_gui()

	def add_body_gui():
		global bodies
		#Funzione per inserire i dati eseguita quando l'utente clicca sul pulsante 'add body'
		def add_body():

			body_type = body_type_var.get()
			try:

				mass = float(mass_entry.get())
				posx = float(posx_entry.get())
				posy = float(posy_entry.get())
				vx = float(vx_entry.get())
				vy = float(vy_entry.get())

				print(bodies)

				if mass <= 0:
					# Viene lanciata un'eccezione 
					raise ValueError("Mass must be greater than zero.")
				
				#Assicura che turtle sia inizializzato
				try:
					turtle.Turtle()
				except turtle.Terminator:
					turtle.Screen()
					

				if body_type == "Planet":
					body = Planet(mass, posx, posy, vx, vy)
				elif body_type == "Star":
					body = Star(mass, posx, posy, vx, vy)
				elif body_type == "Satellite":
					body = Satellite(mass, posx, posy, vx, vy)

				bodies.append(body)
				print(f"corpi:{bodies}")
				messagebox.showinfo("Success", f"{body_type} added successfully!")
				clear_entries()

			except ValueError as e:
				messagebox.showerror("Input error", f"Invalid input: {e}")
			
			return bodies


		#Funzione che cancella il contenuto dei campi input una volta cliccato sul bottone "Add body"
		def clear_entries():
			mass_entry.delete(0, tk.END)
			posx_entry.delete(0, tk.END)
			posy_entry.delete(0, tk.END)
			vx_entry.delete(0, tk.END)
			vy_entry.delete(0, tk.END)

		add_body_frame = tk.Frame(root, bg='black')
		add_body_frame.pack(padx=10, pady=10)


		#Radiobutton per scegliere il tipo di corpo celeste
		tk.Label(add_body_frame, text="Body Type:", fg="white", bg="black", font=("Helvetica", 12)).grid(row=0, column=0)
		body_type_var = tk.StringVar()
		body_type_var.set("Planet")
		planet_radio = tk.Radiobutton(add_body_frame, text="Planet", variable=body_type_var, value="Planet", bg="black", selectcolor="black", indicatoron=1, fg="white", font=("Helvetica", 12))
		planet_radio.grid(row=0, column=1)
		star_radio = tk.Radiobutton(add_body_frame, text="Star", variable=body_type_var, value="Star", bg="black", selectcolor="black", indicatoron=1, fg="white", font=("Helvetica", 12))
		star_radio.grid(row=0, column=2)
		satellite_radio = tk.Radiobutton(add_body_frame, text="Satellite", variable=body_type_var, value="Satellite", bg="black", selectcolor="black", indicatoron=1, fg="white", font=("Helvetica", 12))
		satellite_radio.grid(row=0, column=3)


		#Campi di input per massa, posizione e velocità
		tk.Label(add_body_frame, text="Mass (0.1 to 15 * 10^23 kg):", fg="white", bg="black", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w")
		mass_entry = tk.Entry(add_body_frame, font=("Helvetica", 12), bg="black", fg="white", width=7)
		mass_entry.grid(row=1, column=1, padx=(5, 0))


		tk.Label(add_body_frame, text="Position (x, y):", fg="white", bg="black", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")
		posx_entry = tk.Entry(add_body_frame, font=("Helvetica", 12), bg="black", fg="white", width=7)
		posx_entry.grid(row=2, column=1, padx=(5, 0))
		posy_entry = tk.Entry(add_body_frame, font=("Helvetica", 12), bg="black", fg="white", width=7)
		posy_entry.grid(row=2, column=2)


		tk.Label(add_body_frame, text="Velocity (vx, vy):", fg="white", bg="black", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w")
		vx_entry = tk.Entry(add_body_frame, font=("Helvetica", 12), bg="black", fg="white", width=7)
		vx_entry.grid(row=3, column=1, padx=(5, 0))
		vy_entry = tk.Entry(add_body_frame, font=("Helvetica", 12), bg="black", fg="white", width=7)
		vy_entry.grid(row=3, column=2)


		add_button = tk.Button(add_body_frame, text="Add Body", command=add_body, font=("Helvetica", 12), bg="midnight blue", fg="white")
		add_button.grid(row=4, columnspan=4, pady=10)


	
	global root
	root = tk.Tk()
	root.title("Insert Bodies Manually")
	root.config(bg='black')

	# Chiama la funzione close_manual_window quando l'utente chiude la finestra manualmente
	root.protocol("WM_DELETE_WINDOW", close_manual_window)

	root.geometry("600x400")
	root.resizable(False, False)

	add_body_gui()

	control_frame = tk.Frame(root, bg="black")
	control_frame.pack(pady=20)

	canvas = tk.Canvas(control_frame, width=248, height=80, bg="black", bd=0, highlightthickness=0)
	canvas.grid(row=0, column=0, padx=10)
	
	#Bottone ovale start
	start_button = canvas.create_oval(69, 10, 119, 60, fill="green", outline="white")#x1 = 10, y1 = 10 (angolo superiore sinistro).
	canvas.create_text(94, 35, text="Start", font=("Helvetica", 10), fill="white")

	#L'area cliccabile sarà un rettangolo invisibile, in modo che posso cliccare su ogni punto della superficie del pulsante ovale
	#per far partire la simulazione
	#outline = vuoto (nessun contorno), fill = vuoto (nessun colore di riempimento)
	start_area_invisibile = canvas.create_rectangle(69,10,119,60, outline="", fill="") #10,10 = coordinate superiori sinistra
	
	#Metodo di canvas che porta il  rettangolo sopra tutti gli altri elementi
	canvas.tag_raise(start_area_invisibile)

	#Bottone ovale reset
	reset_button = canvas.create_oval(129, 10, 179, 60, fill="red", outline="white")
	canvas.create_text(154,35, text ="Reset", font=("Helvetica",10), fill = "white")
	reset_area_invisibile = canvas.create_rectangle(129,10,179,60, fill="", outline="")
	canvas.tag_raise(reset_area_invisibile)



	
	'''def on_canvas_click(event):
		print(f"Le coordinate del click {event.x}, {event.y}")
	
	canvas.bind("<Button-1>", on_canvas_click)'''


	#Associa i bottoni alle funzioni
	#Event è un parametro che rappresenta l'oggetto evento generato quando l'utente clicca sul bottone ovale
	canvas.tag_bind(start_area_invisibile, "<Button-1>", lambda event: start_simulation(bodies))
	canvas.tag_bind(reset_area_invisibile, "<Button-1>", lambda event: reset_simulation(bodies))
	
	root.mainloop()
