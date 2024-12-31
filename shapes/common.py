import turtle, random

class Shape(turtle.Turtle):
	def __init__(self, starting_x, starting_y, radius=3):
		super().__init__(shape="circle")
		self.speed(0)
		self.radius = radius
		self.trail_radius = 0.1
		self.starting_x = starting_x
		self.startint_y = starting_y
		self.x = starting_x
		self.y = starting_y
		self.possible_colors = ["magenta", "maroon", "pink", "beige", "aquamarine", "brown", "misty rose", "cyan", "deep pink"]
		self.base_color_name = random.choice(self.possible_colors)
		self.trajectory_color_name = "gray" + str(random.randint(3, 20))
		self.color(self.base_color_name)
		self.shapesize(self.radius, self.radius)
		self.trajectory_completed = 0
	
	def setRadius(self, radius):
		self.radius = radius
		self.shapesize(self.radius, self.radius)
	
	def draw(self):
		self.penup()
		self.goto(self.x, self.y)
	
	def drawTrajectory(self):
		self.hideturtle()
		"""self.penup()
		self.color(self.trajectory_color_name)
		self.goto(self.x, self.y - self.radius)
		self.pendown()
		self.circle(self.trail_radius)
		self.penup()
		self.color(self.base_color_name)"""
		self.color(self.trajectory_color_name)
		self.pendown()
		self.goto(self.x, self.y)