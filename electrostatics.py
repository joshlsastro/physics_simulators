import time
import turtle

# DISCLAIMER: I never included special relativity, which means no magnetism.
# If you use this to simulate electrodynamics, your answer WILL be wrong.

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


class ElectricField(VectorField):
	def set_k(self, k):
		self.k = k

	def distance(self, position1, position2):
		"""Use Pythagorean Theorem to find distance between two positions."""
		x1, y1 = position1[0], position1[1]
		x2, y2 = position2[0], position2[1]
		return ((x2-x1)**2 + (y2-y1)**2) ** 0.5

	def rhat(self, position_body, position_place):
		"""Calculates the unit vector which, when multiplied by the distance,
		gets one from position_body to position_place.
		This is extremely useful for calculating electric field for statics."""
		dx = position_place[0] - position_body[0]
		dy = position_place[1] - position_body[1]
		d = self.distance(position_body, position_place)
		xHat = dx / d
		yHat = dy / d
		return [xHat, yHat]

	def _one_body_value(self, position, body):
		"""Finds electric field from specified body at position."""
		if 'k' not in dir(self):
			raise AttributeError("No k defined!")
		# Coulomb's Law
		d = self.distance(body.position, position)
		if d == 0:
			# Bodies don't exert electric force on themselves
			return [0, 0]
		else:
			r = self.rhat(body.position, position)
			amount = (self.k * body.charge) / (d**2)
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


class PointCharge(BasePhysicsBody):
	"""A Point Charge."""
	def set_charge(self, charge):
		"""Sets charge and stops point charge."""
		self.v_0 = [0,0]
		self.charge = charge

	def force(self):
		return [0,0]

def draw_field_grid(vectorField, separation):
	"""Draw vectorField with a grid separated by separation."""
	global wn
	xTotal, yTotal = wn.screensize()
	for x in range(int(-xTotal/2), int(xTotal/2), separation):
		for y in range(int(-yTotal/2), int(yTotal/2), separation):
			vectorField.draw([x, y])


# <For User>
# Classes of VectorFields used



# Classes of physics bodies with Forces


# Define bodies here

plus = PointCharge([0,30], [0,0], 0, "red")
plus.set_charge(100)
minus = PointCharge([0,-30], [0,0], 0, "blue")
minus.set_charge(-100)

all_bodies = [plus, minus] # Place all bodies here
k = 100 # Coulomb's Constant
resolution = 20 # Resolution of grid
# </For User>

# Running Computation

# Setting up variables
E = ElectricField(all_bodies)
E.set_k(k)
draw_field_grid(E, resolution)
wn.mainloop()
