import time, math

class TimeStep:
	def __init__(self, step=0.01, tempo=1.0):
		self.step = step
		self.elapsed_time = 0.0
		self.tempo = tempo
		self.timer_flags = {}
	
	def nextStep(self):
		time.sleep(self.step)
		self.elapsed_time += self.step
	
	def fastForward(self): ...

	def rewind(self): ...

	def getStepTime(self):
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
		self.tempo = float(tempo_string[:tempo_string.index("x")])