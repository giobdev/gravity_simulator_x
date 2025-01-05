import math

#---
#metodi mancanti
#

class TimeStep:
	MAX_STATE_LOG = 1000 #non loggare piu di 1000 clip
	def __init__(self, step: float = 0.001, tempo: int = 1):
		self.step = step
		self.elapsed_time = 0.0
		self.base_tempo = tempo
		self.tempo = self.base_tempo

		self.timer_flags = {}
		self.clips = {}  #dizionario per memorizzare le clip (snapshot); chiave: time, valore: dati dello screenshot
		self.state_log = []  #log stati per fastF e rewind
		self.current_state = None
	#---GESTIONE TEMPO
	def nextStep(self):
		self.elapsed_time += self.step
	
	def fastForward(self):
		if self.tempo != self.base_tempo:
			self.tempo = self.base_tempo
		else:
			self.tempo = 4 * self.base_tempo

	def rewind(self):
		self.step = -abs(self.step)
	
	def forward(self):
		self.step = abs(self.step)

	def getStepTime(self):
		return self.step
	
	def getAbsStepTime(self):
		return self.step

	def getTempo(self):
		return self.tempo
	
	def getElapsedTime(self):
		return self.elapsed_time
	
	def getElapsedTimeInt(self):
		return math.floor(self.elapsed_time)
	
	def eachTime(self, time, callback):
		name = callback.__name__ + str(id(callback.__self__))
		if name not in self.timer_flags:
			self.timer_flags[name] = 0
		if round(self.getElapsedTime() % time, 1) == 0:
			if self.timer_flags[name] == 1:
				self.timer_flags[name] = 0
				return callback()
		else:
			self.timer_flags[name] = 1

	def setTempo(self, tempo_string="1x"):
		self.tempo = self.base_tempo = int(tempo_string[:tempo_string.index("x")])
		print("tempo:", self.tempo)

	
	#---CLIPS: 'momenti' catturati in modo deciso dall'utente

	#ogni clip include: numerpo di corpi, ID corpi, coeff. stabilita 
	def creaClip(self, bodies, centratura):
		stabilita = self.getElapsedTime() * centratura
		clip = {
			"time_step": self.getElapsedTimeInt(),
			"planet_count": len(bodies),
			"planet_ids" : [id(body) for body in bodies],
			"planet_coords" : None,
			"stabilita": stabilita,
		}

		#salvo la clip nel dizionario (self.clips)
		#chiave: self.getElapsedTimeInt()
		#valore: clip
		self.clips[self.getElapsedTimeInt()] = clip
		return clip
	
	#richiamare una clip dal dizionario self.clips
	#chiave (tempo): time_step
	#nessuna clip per il tempo 'time_step' (int)-> ritorna None
	def getClip(self, time_step):
		return self.clips.get(time_step, None) #get: metodo per cercare un valore in dizionario usando una chiave
	

	#---SALTI


	#usa getClip per riportare il sistema al momento 'time_step'
	#funziona solo se l'utente ha creato una clip per il time_step
	def rewindTo(self, time_step):
		clip = self.getClip(time_step)
		if clip:
			self.elapsed_time = clip["time_step"]
			return clip
		return None

	#predice uno stato futuro e ritnorna il tempo trascorso
	def predState(self, time_elapsed):
		return {"time": time_elapsed} #dizionario chiave("time"):valore(time_elapsed)
	
	#avanza la simulazione velocemente, di n steps, senza i ritardi di time.sleep
	def fastForwardNSteps(self, steps=1): 
		for i in range(steps):
			self.nextStep() #avanza il tempo di 1 passo

			#predizione o calcolo del nuovo stato -> metodo predState
			self.current_state = self.predState(self.elapsed_time)  #aggiorna lo stato corrente con lo stato predetto
			self.state_log.append(self.current_state)
		if len(self.state_log) > self.MAX_STATE_LOG:
			self.state_log = self.state_log[-self.MAX_STATE_LOG:]

	#riavvolge la simulazione di un certo numero di passi
	#servono abbastanza state_log
	def rewindNSteps(self, steps=1):

		#len(...) = quanti stati salvati
		#1: controllare se ci sono abbastanza stati salvati
		if len(self.state_log) >= steps: 
			#2: aggiornare lo stato corrente con lo stato indietro di n steps
			state = self.state_log[-steps] 
			self.elapsed_time = state["time"]
			self.current_state = state["state"]
			#con unpacking -> self.elapsed_time, self.current_state = self.state_log[-steps]

			#3: cancellare tutto il log successivo al nuovo stato corrente
			self.state_log = self.state_log[:len(self.state_log)-steps]
		else:
			print(f"Impossibile riavvolgere di {steps} passi. Disponibili {len(self.state_log)} stati")

