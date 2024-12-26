import turtle

class Shape(turtle.Turtle):
	def __init__(self, starting_x, starting_y, radius=3):
		super().__init__(shape="circle")
		self.radius = radius
		self.trail_radius = 0.5
		self.starting_x = starting_x
		self.startint_y = starting_y
		self.x = starting_x
		self.y = starting_y
		self.color("blue")
		self.shapesize(self.radius, self.radius)
	
	def setRadius(self, radius):
		self.radius = radius
		self.shapesize(self.radius, self.radius)
	
	def setColor(self, color):
		self.color(color)
	
	def draw(self):
		self.penup()
		self.goto(self.x, self.y)
	
	def drawTrail(self):
		self.penup()
		self.goto(self.x, self.y - self.radius)
		self.pendown()
		self.circle(self.trail_radius)
		self.penup()