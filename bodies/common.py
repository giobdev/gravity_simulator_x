import math
from scipy.constants import G

from shapes.common import Shape

class Body(Shape):
	def __init__(self, mass, starting_x, starting_y, starting_speed_x=0.0, starting_speed_y=0.0):
		super().__init__(starting_x, starting_y)
		self.mass = mass
		self.speed_x = starting_speed_x
		self.speed_y = starting_speed_y
		self.acceleration_x = 0.0
		self.acceleration_y = 0.0

	def updateSpeed(self, delta_t):
		self.speed_x += self.acceleration_x * delta_t
		self.speed_y += self.acceleration_y * delta_t
		self.acceleration_x = 0
		self.acceleration_y = 0

	def updatePosition(self, delta_t):
		self.updateSpeed(delta_t)
		self.x += self.speed_x * delta_t
		self.y += self.speed_y * delta_t

	def applyForceIn(self, force_x, force_y, mass_oom=10**10):
		self.acceleration_x += force_x / self.mass * mass_oom
		self.acceleration_y += force_y / self.mass * mass_oom

	def applyForceOut(self, other_mass, other_x, other_y, mass_oom=10**10, distance_oom=10**2):
		mass_1 = self.mass * mass_oom
		mass_2 = other_mass * mass_oom
		distance_x = (other_x - self.x) * distance_oom
		distance_y = (other_y - self.y) * distance_oom
		distance = math.sqrt(distance_x**2 + distance_y**2)
		if distance == 0:
			return 0.0, 0.0
		force_magnitude = G * mass_1 * mass_2 / distance ** 2
		unit_x = distance_x / distance
		unit_y = distance_y / distance
		force_x = -force_magnitude * unit_x
		force_y = -force_magnitude * unit_y
		return force_x, force_y

	def updateAll(self, delta_t, time_speed=1.0):
		self.updatePosition(delta_t * time_speed)