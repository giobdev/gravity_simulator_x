from bodies.planet import *
from bodies.star import *
from bodies.satellite import *
from time_manager import TimeStep
from physics_manager import PhysicsManager

class Trajectory():
	def __init__(self, bodies, timeStep):
		self.bodies = [self.copyBody(body) for body in bodies]
		self.physicsManager = PhysicsManager(self.bodies, timeStep)
	
	def copyBody(self, body):
		if body.body_name == "planet":
			return Planet(mass=body.mass, starting_x=body.x, starting_y=body.y, starting_speed_x=body.speed_x, starting_speed_y=body.speed_y, starting_acceleration_x=body.acceleration_x, starting_acceleration_y=body.acceleration_y)
		if body.body_name == "star":
			return Star(mass=body.mass/body.base_oom, starting_x=body.x, starting_y=body.y, starting_speed_x=body.speed_x, starting_speed_y=body.speed_y, starting_acceleration_x=body.acceleration_x, starting_acceleration_y=body.acceleration_y)
		if body.body_name == "satellite":
			return Satellite(mass=body.mass*body.base_oom, starting_x=body.x, starting_y=body.y, starting_speed_x=body.speed_x, starting_speed_y=body.speed_y, starting_acceleration_x=body.acceleration_x, starting_acceleration_y=body.acceleration_y)