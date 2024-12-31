import math

class TimeStep:
	def __init__(self, step: float = 0.001, tempo: int = 1):
		self.step = step
		self.elapsed_time = 0.0
		self.base_tempo = tempo
		self.tempo = self.base_tempo
		self.timer_flags = {}
	
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