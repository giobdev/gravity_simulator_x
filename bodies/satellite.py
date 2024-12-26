from bodies.common import *

class Satellite(Body):
	def __init__(self, mass=10, starting_x=10, starting_y=10, starting_speed_x=0.0, starting_speed_y=0.0, base_oom=10**6):
		super().__init__(mass / base_oom, starting_x, starting_y, starting_speed_x, starting_speed_y)
		self.setRadius(mass/15)
		self.setColor("grey")