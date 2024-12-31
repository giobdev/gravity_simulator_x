class Camera():
	def __init__(self):
		...
	
	def recenter(self, body_to_follow_i, bodies):
		delta_x = bodies[body_to_follow_i].x
		delta_y = bodies[body_to_follow_i].y
		for body in bodies:
			body.x -= delta_x
			body.y -= delta_y