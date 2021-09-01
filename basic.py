import time
import turtle

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

# <For User>
# Classes of physics bodies with Forces

# Here's an example of modifying a class. You need to change the force from the default.
# It can be whatever you want.
class SimpleHarmonicOscillator(BasePhysicsBody):
    """Simple harmonic osciallator"""
    def force(self):
        self.turtle.pendown()
        k = 2
        F_spring = -k*self.position[0]
        return [F_spring, 0]

class DampedOscillator(BasePhysicsBody):
    """Damped oscillator"""
    def force(self):
        self.turtle.pendown()
        k = 1
        b = 10
        F_spring = -k*self.position[0]
        F_res = -b*self.velocity[0]
        return [F_spring + F_res, 0]

class Planet(BasePhysicsBody):
    """A planet that orbits the center of the screen"""
    def force(self):
        self.turtle.pendown()
        GM = 1e6
        d = (self.position[0]**2+self.position[1]**2) ** (1/2)
        g = -GM/d**2
        F = self.mass*g
        return [F*self.position[0]/d, F*self.position[1]/d]

# Define bodies here
spring = SimpleHarmonicOscillator([50, 0], [0, 0], 1, "gray", "square")

all_bodies = [spring] # Place all bodies here
time_step = 0.03 # Time step you want to use
total_simulation_time = 30 # Total simulation time
real_time_per_time_step = 0 # Number of actual seconds spent sleeping per time step
time_steps_per_frame = 1 # Number of time steps per frame; bigger number means faster, but more choppy
# </For User>

# Running Simulation
turtle.tracer(time_steps_per_frame)

sim_time = 0
while sim_time < total_simulation_time:
    print("Sim Time:", sim_time)
    time.sleep(real_time_per_time_step)
    for body in all_bodies:
        body.update(time_step)
    sim_time += time_step
