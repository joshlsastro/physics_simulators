import time
import turtle

wn = turtle.Screen()

class BasePhysicsBody(object):
    """Base Class for Physics Body."""
    def __init__(self, x_0, v_0, m, color=None, shape='turtle'):
        self.turtle = turtle.Turtle()
        self.turtle.shape(shape)
        if color != None:
            self.turtle.color(color)
        self.turtle.speed(0) # As fast as possible; update() takes care of motion
        self.turtle.penup()
        self.position = x_0
        self.velocity = v_0
        self.mass = m
        self.turtle.goto(x_0)

    def force(self):
        """Up to user."""
        return [0, 0]

    def update(self, time_step):
        """Updates all attributes for one time_step."""
        a = [0,0]
        F = self.force()
        for i in [0,1]: # We have to update x and y
            a[i] = self.force()[i] / self.mass
            self.velocity[i] = self.velocity[i] + a[i]*time_step
            self.position[i] = self.position[i] + self.velocity[i]*time_step # I'm lazy
        self.turtle.goto(self.position) # Comment out the goto if you need the simulation to run really fast; you won't get the animation



class VectorField(object):
    """A vector field."""
    def __init__(self, distribution):
        """Initializes VectorField where distribution is a list of BasePhysicsBody objects."""
        self.distribution = distribution
        self.ped = turtle.Turtle()
        self.ped.hideturtle()
        self.ped.speed(0)
        self.ped.penup()

    def value(self, position):
        """Returns value of vector field at position. Returns 0 by default."""
        return [0,0]

    def draw(self, position):
        """Draws vector field value at position."""
        # Getting value at position
        vector = self.value(position)
        x = vector[0]
        y = vector[1]
        # Using self.ped to draw vector
        self.ped.goto(position[0], position[1])
        self.ped.pendown()
        self.ped.goto(position[0]+x, position[1]+y)
        self.ped.penup()

def draw_field_grid(vectorField, separation):
	"""Draw vectorField with a grid separated by separation."""
	global wn
	xTotal, yTotal = wn.screensize()
	for x in range(int(-xTotal/2), int(xTotal/2), separation):
		for y in range(int(-yTotal/2), int(yTotal/2), separation):
			vectorField.draw([x, y])


# <For User>
# Classes of VectorFields used

class GravitationalField(VectorField):
	def setG(self, G):
		self.G = G

	def distance(self, position1, position2):
		"""Use Pythagorean Theorem to find distance between two positions."""
		x1, y1 = position1[0], position1[1]
		x2, y2 = position2[0], position2[1]
		return ((x2-x1)**2 + (y2-y1)**2) ** 0.5

	def rhat(self, position_body, position_place):
		"""Calculates the unit vector which, when multiplied by the distance,
		gets one from position_body to position_place.
		This is extremely useful for calculating gravity."""
		dx = position_place[0] - position_body[0]
		dy = position_place[1] - position_body[1]
		d = self.distance(position_body, position_place)
		xHat = dx / d
		yHat = dy / d
		return [xHat, yHat]

	def _one_body_value(self, position, body):
		"""Finds gravitational field from specified body at position."""
		if 'G' not in dir(self):
			raise AttributeError("No G defined!")
		# Newton's Law of Gravity
		d = self.distance(body.position, position)
		if d == 0:
			# Bodies don't exert gravity on themselves
			return [0, 0]
		else:
			r = self.rhat(body.position, position)
			amount = -(self.G * body.mass) / (d**2)
			return [amount*r[0], amount*r[1]]


	def value(self, position):
		all_vectors = []
		for body in self.distribution:
			all_vectors.append(self._one_body_value(position, body))
		# Adding up vectors
		x = 0
		y = 0
		for vector in all_vectors:
			x += vector[0]
			y += vector[1]
		return [x, y]

# Classes of physics bodies with Forces

class GravityBody(BasePhysicsBody):
	"""BasePhysicsBody with gravity."""
	def set_field(self, gravitational_field):
		"""Sets gravitational field."""
		self.g_field = gravitational_field

	def force(self):
		self.turtle.pendown()
		g = self.g_field.value(self.position)
		return [self.mass*g[0], self.mass*g[1]]

# Define bodies here

body_1 = GravityBody([0,-80], [0,4], 8000, "green", "circle")
body_2 = GravityBody([-(3**0.5)*40,40], [-2,4], 8000, "blue", "circle")
body_3 = GravityBody([(3**0.5)*40,40], [2,-8], 8000, "red", "circle")

all_bodies = [body_1, body_2, body_3] # Place all bodies here
G = 1 # Newton's Gravitational Constant
time_step = 0.001 # Time step you want to use
total_simulation_time = 90 # Total simulation time
real_time_per_time_step = 0 # Number of actual seconds per time step
time_steps_per_frame = 200 # Number of time steps per frame; bigger number means faster, but more choppy
# </For User>

# Running Simulation

# Setting up variables
turtle.tracer(time_steps_per_frame)
g_field = GravitationalField(all_bodies)
g_field.setG(G)

# Setting fields for normal bodies
for body in all_bodies:
	if body.__class__ == GravityBody:
		body.set_field(g_field)

# Actual Simulations
sim_time = 0
while sim_time < total_simulation_time:
    print("Sim Time:", sim_time)
    time.sleep(real_time_per_time_step)
    for body in all_bodies:
        body.update(time_step)
    sim_time += time_step
