class PhysicsManager:
	def __init__(self, bodies, timeStep):
		self.distance_oom = 10 ** 8
		self.mass_oom = 10 ** 11
		self.bodies = bodies
		self.timeStep = timeStep
	
	def addBody(self, body):
		self.bodies.append(body)
	
	def removeBody(self, body):
		self.bodies.remove(body)
	
	def applyAllForces(self):
		for body in self.bodies:
			for other_body in [b for b in self.bodies if b != body]:
				force_x, force_y = body.applyForceOut(
					other_body.mass, 
					other_body.x, 
					other_body.y, self.mass_oom, self.distance_oom)
				other_body.applyForceIn(force_x, force_y, self.mass_oom)