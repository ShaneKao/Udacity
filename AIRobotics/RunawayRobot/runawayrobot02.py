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
def getWeight(actualmoved, robotmoved):
	prob = 1.0
	#print "actual moved is " + str(actualmoved) + " and robot moved is " + str(robotmoved)
	#if abs(actualmoved - robotmoved ) < 10:
	#	print "Dif is " + str(actualmoved - robotmoved )
	
	pr = exp(- ((actualmoved - robotmoved) ** 2) / (measurement_noise ** 2) / 2.0) / sqrt(2.0 * pi * (measurement_noise ** 2)) 
	#print "Prob is " + str(pr)
	#if pr > .1:
	#	print "Prob of " + str(pr) + " robot moved " + str(robotmoved) + " and measured move is " + str(actualmoved)
	return pr

	
def estimate_next_pos(measurement, OTHER = None):
	p = []
	dx = 0
	dy = 0
	heading = 0
	v = 0
	turning = random.gauss(0,2*pi)
	N = 1000
	worldsize = 10
	lastPosition = [0,0]
	lastHeading = 0
	initialized = False
	if OTHER == None:
		#print "initializing p for 1000"
		
		maxWeight = -1
		wIndex = -1
		# do initial position
		for i in range(N):
			#tRobot = robot(random.randint(5), random.randint(5))
			#print "RAndint " + str(random.randint(-50,50)) + ", " + str(random.randint(-50,50))
			rHeading = random.gauss(0,2*pi)
			rTurning = random.gauss(0,2*pi)
			myRobot = robot(random.randint(-worldsize,worldsize), random.randint(-worldsize,worldsize), random.gauss(0,2*pi), random.gauss(0,2*pi), random.randint(1,5))
			myRobot.set_noise(0.0, 0.0, measurement_noise)
			turning = random.gauss(0, 2*pi)
			
			
			p1 = myRobot.sense()
		
			dif = distance_between(p1,  measurement)
			w = getWeight( 0, dif  )
			
			if w > maxWeight:
				wIndex = i
				maxWeight = w
				
			p.append(myRobot)
			dx = 1
			dy = 1
		
	
		print "windex = " + str(wIndex)
		
		closestPos = p[wIndex].sense()
		
		OTHER = [measurement, heading,  p]
		fpos = closestPos
		#print "First measurement " + str(measurement[0]) + ", " + str(measurement[1])
		#print "First particle was " + str(closestPos[0]) + ", " + str(closestPos[1])
		#print "First prediction " + str(fpos[0]) + ", " + str(fpos[1])
		#print "*****************"
		return [fpos,  OTHER ]
		
	else:
		initialized = True
		lastPosition, lastHeading, p = OTHER
		print "MEAS: " + str(lastPosition[0]) + ", " + str(lastPosition[1]) + "  this measurement " + str(measurement[0]) + ", "  + str(measurement[1])

		v = distance_between(lastPosition, measurement)
		dy = measurement[1] - lastPosition[1]
		dx = measurement[0] - lastPosition[0]
		heading = atan(dy/dx) 
		turning = ( heading - lastHeading ) % (2 * pi)
		heading = heading % 2*pi
		# print "calculated heading " + str(heading)
		# print "last heading is " + str(lastHeading)
		# print "difference and/or turning is " + str(turning)
		
		# move each robot
		for i in range(N):
			
			p[i] = robot(p[i].sense()[0], p[i].sense()[1], heading, 0)
			p[i].set_noise(0.0, 0.0, measurement_noise)
			p[i].move(turning, v)

		
	
	#print "******"
	minpoint = [0,0]
	mindis = 100
	closestIndex = -1
	weightIndex = -1
	maxWeight = 0
	
	wts = []
	
	# calculate weights based on the difference to the measurement
	for i in range(N):
		pos = p[i].sense()
		w = getWeight(0 , distance_between(measurement, pos))
	
		wts.append(w)
		if w > weightIndex:
			weightIndex = i
			maxWeight = w
			minpoint = pos
			
	
	print "Max w = " + str(max(wts))
	# print "Max weight was " + str(p[i].sense()[0]) + ", " + str(p[i].sense()[1])
	#print "min distance is " + str(mindis)
	print "best point is " + str(minpoint[0]) + ", " + str(minpoint[1])
	print " going to move with heading " + str(heading) + " and turning " + str(turning) + " by distance " + str(v)
	nextRobot = p[weightIndex]
	#print "next robot moving by " + str(v) + " and heading " + str(heading)
	nextRobot.move(turning, v)
	if distance_between(minpoint, nextRobot.sense()) > v + 1.5:
		print "The moved distance was " + str(distance_between(minpoint, nextRobot.sense()))
		print "Error"
		return
	
	# You must return xy_estimate (x, y), and OTHER (even if it is None) 
	# in this order for grading purposes.
	xy_estimate = nextRobot.sense()
	print "Predict " + str(xy_estimate[0]) + ", " + str(xy_estimate[1])
	
	OTHER = [measurement, heading,  p]
	print "************"

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
test_target.set_noise(0.0, 0.0, measurement_noise)

#demo_grading(naive_next_pos, test_target)
demo_grading(estimate_next_pos, test_target)




