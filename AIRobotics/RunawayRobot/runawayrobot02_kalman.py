#!/usr/bin/python


# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess 
# for the robot's next position.
#
# ----------
# YOUR JOB
#
# Complete the function estimate_next_pos. You will be considered 
# correct if your estimate is within 0.01 stepsizes of Traxbot's next
# true position. 
#
# ----------
# GRADING
# 
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import * # Check the matrix.py tab to see how this works.
import random

# This is the function you have to write. Note that measurement is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
def getWeight():
	prob = 1.0
	#print "actual moved is " + str(actualmoved) + " and robot moved is " + str(robotmoved)
	#if abs(actualmoved - robotmoved ) < 10:
	#	print "Dif is " + str(actualmoved - robotmoved )
	#pr = exp(- ((actualmoved - robotmoved) ** 2) / (measurement_noise ** 2) / 2.0) / sqrt(2.0 * pi * (measurement_noise ** 2)) 
	return 1/distance

def better(thelist, samples, wmax):
    thisIndex = random.randint(0,len(thelist)-1)
    B = 0
    newp = []
    B = B + random.uniform(0, 2*wmax)
	
    for i in range (len(thelist)):
        windex = thelist[thisIndex]
        #print "windex is " + str(windex)

        if windex < B:
            B =  B - windex
            thisIndex = thisIndex + 1
            if thisIndex > (len(thelist) - 1):
                thisIndex = 0
        else:

            newp.append(samples[thisIndex])
            return samples[thisIndex]
			
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
	return [0, 0]

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
	return 0
	
def predict():
	return [0, 0]
	

def estimate_next_pos(measurement, OTHER = None):
	mu = 0
	sigma = 0
	counter = 0
	lastPosition = [0, 0]
	tmu = 0
	tsig = 0
	lheading = 0
	heading = 0
	tsig = 0
	tmu = 0
	lastheading = 0
    
 	if OTHER == None:
		sigma = 10000
		tsig = 10000
		       
	if OTHER != None:
		mu, sigma, lastheading, tmu, tsig, counter, lastPosition = OTHER
	 
	counter += 1
	#print "Measure " + str(measurement[0]) + ", " + str(measurement[1])
	#print "*************************" + str(counter)
	#print "read mu of " + str(mu) + " and turning Mu of " + str(tmu)
	db = distance_between(lastPosition, measurement)
	#print "distance is " + str(db)
	
	dy = measurement[1] - lastPosition[1]
	dx = measurement[0] - lastPosition[0]
	#print " dx = " + str(dx) + " dy = " + str(dy)
	thisheading = calculateHeading(dx, dy)
	
	#print "new heading is " + str(thisheading) + " last heading is " + str(lastheading)
	turning = (thisheading - lastheading)  
	if turning < 0:
		turning = lastheading - thisheading
	
	#print "Q: " + str(getQuadrant(thisheading))
	
	if getQuadrant(lastheading) == 4 and getQuadrant(thisheading) == 1:
		turning = thisheading + ( pi*2 - abs(lastheading))
		#print "changed turning heading to be " + str(turning)
	
	turning = turning % (2 * pi)
	#print "calc new turn of " + str(turning) + " for iteration " + str(counter)
	
	

	mu, sigma = update(mu, sigma, db, measurement_noise)
	tmu, tsig = update(tmu, tsig, turning, measurement_noise)
	#print "new mu is " + str(mu) + " turning mu is " + str(tmu)
	
	tRobot = robot(measurement[0], measurement[1], heading)
	#tRobot.set_noise(0.0, 0.0, measurement_noise)
	tRobot.move(tmu, mu)
	xy_estimate = tRobot.sense()
	#print "Predict " + str(xy_estimate[0]) + ", " + str(xy_estimate[1])
	
	OTHER = [mu, sigma, thisheading, tmu, tsig, counter, measurement ]
	

	return xy_estimate, OTHER
	
# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any 
# information that you want. 
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    while not localized and ctr <= 5000:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 5000:
            print "Sorry, it took you too many steps to localize the target."
    return localized

# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER 
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
measurement_noise = 0.05 * test_target.distance
# print "measurement noise is " + str(measurement_noise)
test_target.set_noise(0.0, 0.0, measurement_noise)
# test_target.set_noise(0.0, 0.0, 0.0)
#demo_grading(naive_next_pos, test_target)
demo_grading(estimate_next_pos, test_target)




