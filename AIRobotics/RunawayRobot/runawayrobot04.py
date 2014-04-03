#!/usr/bin/python

# ----------
# Part Three
#
# Now you'll actually track down and recover the runaway Traxbot. 
# In this step, your speed will be about twice as fast the runaway bot,
# which means that your bot's distance parameter will be about twice that
# of the runaway. You can move less than this parameter if you'd 
# like to slow down your bot near the end of the chase. 
#
# ----------
# YOUR JOB
#
# Complete the next_move function. This function will give you access to 
# the position and heading of your bot (the hunter); the most recent 
# measurement received from the runaway bot (the target), the max distance
# your bot can move in a given timestep, and another variable, called 
# OTHER, which you can use to keep track of information.
# 
# Your function will return the amount you want your bot to turn, the 
# distance you want your bot to move, and the OTHER variable, with any
# information you want to keep track of.
# 
# ----------
# GRADING
# 
# We will make repeated calls to your next_move function. After
# each call, we will move the hunter bot according to your instructions
# and compare its position to the target bot's true position
# As soon as the hunter is within 0.01 stepsizes of the target,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot. 
#
# As an added challenge, try to get to the target bot as quickly as 
# possible. 

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
# This function will be called after each time the target moves. 
	#print "target turn is " + str(target.turning)
	# The OTHER variable is a place for you to store any historical information about
	# the progress of the hunt (or maybe some localization information). Your return format
	# must be as follows in order to be graded properly.
	#print target_measurement
	#print "turn"
	#print target.turning
	mu = 0
	sigma = 10000
	
	tmu = 0
	tsigma = 10000
	lastPosition = target_measurement
	lastHeading = 0
	thisheading = 0
	counter = 0
	if OTHER != None:
		lastPosition, lastHeading, mu, sigma, tmu, tsigma, counter = OTHER
	
	counter += 1
	#print "read tmu = " + str(tmu) + " mu=" + str(mu) + " sigma = " + str(sigma)
	mu, sigma = update(mu, sigma, distance_between(lastPosition, target_measurement), measurement_noise)
	moved = distance_between(lastPosition, target_measurement)
	#print "Mesurement is " + str(target_measurement[0]) + ", " + str(target_measurement[1])
	#print "**************************"
	#print "Distance is " + str(distance_between(hunter_position, target_measurement)) + " after moving " + str(moved)
	dy = target_measurement[1] - lastPosition[1]
	dx = target_measurement[0] - lastPosition[0]
	
	if dx == 0 and dy == 0:
		heading = 0
	else:
		thisheading = calculateHeading(dx, dy)
		thisheading = get_heading( lastPosition, target_measurement)
	
	
	turning = thisheading - lastHeading
	
	if lastHeading > 0 and thisheading < 0:
		turning = (pi - abs(thisheading)) + (pi - lastHeading )
	
	if lastHeading < 0 and thisheading > 0:
		turning = thisheading + abs(lastHeading)

	tmu, tsigma = update(tmu, tsigma, turning, measurement_noise)
	
	
	#print "need to head " + str(headingNeeded)
	#print "need to head " + str(headingNeeded)

	
	
	tempRobot = robot(target_measurement[0], target_measurement[1], thisheading)
	tempRobot.move(tmu, mu)
	dtt = distance_between(hunter_position, tempRobot.sense())
	#print "Dtt is " + str(dtt)
	#print "Looping with tmu " + str(tmu)
	
	bestpoint = tempRobot.sense()
	
	#
	for i in range(30):
		tempRobot.move(tmu, mu)
		thisdtt = distance_between(hunter_position, tempRobot.sense())
		if thisdtt < dtt:
			dtt = thisdtt
			bestpoint = tempRobot.sense()
			#print "found a better dtt with " + str(thisdtt)
			#print "at point " + str(bestpoint)
    

	#tempRobot.set_noise(0.0, 0.0, measurement_noise)
	#sigma += measurement_noise
	#tsigma += measurement_noise
	
	headingNeeded = get_heading(hunter_position, bestpoint)
	turn2 = headingNeeded - hunter_heading
	

	# print "Chase Robot is at " + str(hunter_position[0]) + ", " + str(hunter_position[1]) + " heading " + str(hunter_heading)
	# print "Target is at " + str(target_measurement[0]) + ", " + str(target_measurement[1]) + " calc heading  " + str(thisheading)
	# print "Predict " + str(bestpoint[0]) + ", " + str(bestpoint[1])
	# print "Chase should head " + str(headingNeeded)
	# print "Chase robot is " + str(dtt) + " away from prediction"
	# print "****"

	#print "Distance to prediction " + str(dtt)
	#print "Chase Difference = " + str(cX) + ", " + str(cY)
	#print "Truncated turn would be " + str(turn2)
	chaseDistance = distance_between(hunter_position, target_measurement)
	distance = 0
	#print "Chase distance is " + str(chaseDistance)
	if dtt >= max_distance:
		distance = max_distance
	else:
		distance = dtt
	
	#distance = max_distance
	turning = turn2
	
	if hunter_heading > 0 and headingNeeded < 0:
		turning = (pi - abs(headingNeeded)) + (pi - hunter_heading )
	
	if hunter_heading < 0 and headingNeeded > 0:
		turning = headingNeeded + abs(hunter_heading)
		
	#print "Using turn " + str(turning) + " and distance = " + str(distance)

	OTHER = [target_measurement, thisheading,  mu, sigma, tmu, tsigma, counter]
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
    max_distance = 0.98 * target_bot.distance # 1.94 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0

    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:

        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        print "separation is " + str(separation)
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


def demo_grading2(hunter_bot, target_bot, next_move_fcn, OTHER = None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we 
    will grade your submission."""
    max_distance = 1.94 * target_bot.distance # 1.94 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0
    print "tolerance is " + str(separation_tolerance)
    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:

        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        #print "Separation is " + str(separation)
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
measurement_noise = .05*target.distance
target.set_noise(0.0, 0.0, measurement_noise)

hunter = robot(-10.0, -10.0, 0.0)

# print demo_grading(hunter, target, naive_next_move)
demo_grading(hunter, target, next_move)






