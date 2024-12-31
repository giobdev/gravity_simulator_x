class Camera():
	def __init__(self, body_to_follow):
		self.body_to_follow = body_to_follow
	
	def recenter(self, bodies):
		delta_x = self.body_to_follow.x
		delta_y = self.body_to_follow.y
		for body in bodies:
			body.x -= delta_x
			body.y -= delta_y