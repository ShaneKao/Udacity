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
		#print "updating heading from " + str(heading)
		heading = 1.571 + abs( heading + 1.571)
	elif dx < 0 and dy < 0:
		#print "quadrant 3 heading from " + str(heading)
		heading = pi + heading
	elif dx > 0 and dy < 0:
		#print "quadrant 4 update"
		heading = 4.712 +  1.571 + heading
	
	return heading

def estimate_next_pos_test(measurement, OTHER = None):
	return [0,0] , OTHER
	
def estimate_next_pos(measurement, OTHER = None):

	p = []
	dx = 0
	dy = 0
	heading = 0
	v = 0
	turning = random.gauss(0,2*pi)
	N = 100
	worldsize = 10
	lastPosition = [0,0]
	lastHeading = 0
	initialized = False
	newp = []
	counter = 0
	turning = 0
	turns = []
	distances = []
	
	#lastPosition, lastHeading, p, counter = "", "", ""
	if OTHER != None:
		lastPosition, lastHeading, p, counter, turns, distances = OTHER
		
	if OTHER == None or counter < 4:
		counter +=1
		maxWeight = -1
		wIndex = -1
		# do initial position
		
		
		if counter > 1:
			dy = measurement[1] - lastPosition[1]
			dx = measurement[0] - lastPosition[0]
			heading = calculateHeading(dx, dy)
			heading = angle_trunc(heading)
			turning = heading - lastHeading
			v = distance_between(lastPosition, measurement)

			print "First turning is " + str(turning)
			print "First v is " + str(v)
			
		# get random positions
		p = []
		for i in range(N):
			rHeading = random.gauss(0,2*pi)
			rTurning = random.gauss(0,2*pi)
			rx = random.gauss(measurement[0], measurement_noise)
			ry = random.gauss(measurement[1], measurement_noise)
			myRobot = robot(rx , ry,  random.gauss(heading,measurement_noise * 2*pi), random.gauss(0,2*pi), random.randint(1,5))
			myRobot.set_noise(0.0, 0.0, 0.0)
			p.append(myRobot)
		
		
		closestPoint = 100
		closestIndex = 0

		for i in range(N):
			p[i].move(turning, v)
			
		closestPos = p[closestIndex].sense()
		OTHER = [measurement, heading,  p, counter, turns, distances]
		fpos = closestPos
		return closestPos, OTHER
		
	else:
		#print "**********************"
		initialized = True
		lastPosition, lastHeading, p, counter, turns, distances = OTHER
		print "MEAS: " + str(lastPosition[0]) + ", " + str(lastPosition[1]) + "  this measurement " + str(measurement[0]) + ", "  + str(measurement[1])
		print "*********************************************"
		v = distance_between(lastPosition, measurement)
		
		distances.append(v)
		averageV = sum(distances)/len(distances)
		
		#print " v is " + str(v) + " avg v is " + str(sum(distances)/len(distances))
		dy = measurement[1] - lastPosition[1]
		dx = measurement[0] - lastPosition[0]
		heading = calculateHeading(dx, dy)
			
		#print "HEADING " + str(heading) + " or truncated of " + str(heading)
		turning = ( heading - lastHeading ) % (2 * pi)
		turns.append(turning)
		print "turn size is " + str(len(turns))
		avgturn = sum(turns)/ len(turns)
		
		newp = p
		
		#for i in range(N):
		#	p[i].move(avgturn, averageV)

		
	closestIndex = -1
	weightIndex = -1
	maxWeight = 0

	# wts is new weights
	wts = []
	p.sort()
	for i in range(N):
		pos = newp[i].sense()
		dx = pos[0] - measurement[0]
		dy = pos[1] - measurement[1]
		diffAngle = calculateHeading(dx, dy)
		
		tw =  abs(( 1/dx) * ( 1 / dy ) * (1 / ( heading - diffAngle)))
		print "Weighting " + str(pos[0]) + ", " + str(pos[1]) + " weight " + str(tw)
		wts.append(tw)
		if tw > maxWeight:
			weightIndex = i
			maxWeight = tw
			minpoint = pos
			
	#print "Best point to move is " + str(minpoint[0]) + ", " + str(minpoint[1])
	
	p3 = []
	index = int(random.random() * N)
	
	beta = 0.0
	
	mw = max(wts)
	
	for i in range(N):
		beta += random.random() * 2.0 * mw
		while beta > wts[index]:
			beta -= wts[index]
			index = (index + 1) % N
			
		p3.append(newp[index])


	for i in range(N):
		p3[i].move(turning, v)
	
	x = 0.0
	y = 0.0
	for i in range(N):
		x += p3[i].x
		y += p3[i].y
		
	#print "total x is " + str(x/len(p))
	#print "total y is " + str(y/len(p))
	p = p3
	p3.sort()
	for i in range(N):
		print "Sampled " + str(p3[i].sense()[0]) + ", " + str(p3[i].sense()[1])

	xy_estimate = [ x / len(p3) , y / len(p3)]
	print "Predict " + str(xy_estimate[0]) + ", " + str(xy_estimate[1])
	OTHER = [measurement, heading,  p, counter, turns, distances]

	xy_estimate = [x/len(p), y/len(p)]
 
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




