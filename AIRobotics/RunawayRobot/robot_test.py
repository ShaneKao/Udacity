#!/usr/bin/python

from robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import * # Check the matrix.py tab to see how this works.
import random


print "Creating robot"
myrobot = robot(0,0)

print myrobot.sense()

print "Moving 1"
myrobot.move(0,1)

print myrobot.sense()

myrobot.move(0,1)

print "Moving again"

print myrobot.sense()
