#!/usr/bin/python
# ----------
# Part Five
#
# This time, the sensor measurements from the runaway Traxbot will be VERY 
# noisy (about twice the target's stepsize). You will use this noisy stream
# of measurements to localize and catch the target.
#
# ----------
# YOUR JOB
#
# Complete the next_move function, similar to how you did last time. 
#
# ----------
# GRADING
# 
# Same as part 3 and 4. Again, try to catch the target in as few steps as possible.

from robot import *
from math import *
from matrix import *
import random
def calculateHeading(dx, dy):
	heading = atan(dy/dx)

	if dx < 0 and dy > 0:
		#print "updating heading for quadrant 2 " + str(heading)
		heading = pi/2 + ( pi/2 - abs(heading))
	elif dx < 0 and dy < 0:
		#print "quadrant 3 heading from " + str(heading)
		heading = pi + heading
	elif dx > 0 and dy < 0:
		#print "quadrant 4 update"
		heading = 4.712 +  1.571 + heading
	
	return heading

def update(mean1, var1, mean2, var2):
	#print "var 1 = " + str(var1) + " var2 = " + str(var2)
	new_mean = (var2 * mean1 + var1 * mean2) / (var1 + var2)
	new_var = 1/(1/var1 + 1/var2)
	return [new_mean, new_var]
	
def predict():
	return 0
	
def getQuadrant(a):
	if a >= 0 and a <= (pi/2):
		#print "angle " + str(a) + " is less than " + str(pi/2)
		return 1
	elif a > pi/2 and a <= pi:
		return 2
	elif a > pi and a <= 3*pi/2:
		return 3
	else:
		return 4
def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):		
	counter = 0
	turning = 0
	distance = 0
	lastPostiion = [0,0]
	particles = []
	
	N = 100
	if OTHER != None:
		print "Measurement = " + str(target_measurement)
		counter, lastPosition, particles = OTHER
		particles.sort()
		for i in range(len(particles)):
			print "Particle " + str(i) + " at " + str(particles[i].x) + ", " + str(particles[i].y) + " distance "  + str(distance_between(target_measurement, particles[i].sense()))
			
		return

	else:

		for i in range(50):
			rx = random.gauss(target_measurement[0], measurement_noise)
			ry = random.gauss(target_measurement[1], measurement_noise)
			rheading = random.gauss(0,2*pi)
			
			tempRobot = robot(rx, ry, rheading)
			#tempRobot.set_noise(0.0, 0.0, measurement_noise)
			particles.append(tempRobot)
		
		max_w = 0
		max_index = -1
		for j in range(len(particles)):
			dx = abs(particles[j].x - target_measurement[0])
			dy = abs(particles[j].y - target_measurement[1])
			w = 1/dx * ( 1/dy)
			print "Particle " + str(j) + " at " + str(particles[j].x) + ", " + str(particles[j].y) + " distance "  + str(distance_between(target_measurement, particles[j].sense()))  + " weight = " + str(w)
			if w > max_w:
				max_w = w
				max_index = j
			

		
		print "Measurement = " + str(target_measurement)

			
		print "Max weight is " + str(max_w) + " distance is " + str(distance_between(target_measurement, particles[max_index].sense())) + " index  = " + str(max_index)
		return
			
	counter += 1
	
	OTHER = [counter, target_measurement, particles]
	print "Counter " + str(counter)
	return turning, distance, OTHER

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER = None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we 
    will grade your submission."""
    max_distance = 0.97 * target_bot.distance # 0.97 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0
    #print "target box move is " + str(target_bot.distance)
    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:

        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        if separation < separation_tolerance:
            print "You got it right! It took you ", ctr, " steps to catch the target."
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)
        
        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()

        ctr += 1            
        if ctr >= 1000:
            print "It took too many steps to catch the target."
    return caught



def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading

def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all 
    the target measurements, hunter positions, and hunter headings over time, but it doesn't 
    do anything with that information."""
    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings) # now I can keep track of history
    else: # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER # now I can always refer to these variables
    
    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning =  heading_difference # turn towards the target
    distance = max_distance # full speed ahead!
    return turning, distance, OTHER

target = robot(0.0, 10.0, 0.0, 2*pi / 30, 1.5)
measurement_noise = 2.0*target.distance # VERY NOISY!!
target.set_noise(0.0, 0.0, measurement_noise)
print "measurement noise is " + str(measurement_noise)
hunter = robot(-10.0, -10.0, 0.0)

# print demo_grading(hunter, target, naive_next_move)
demo_grading(hunter, target, next_move)




