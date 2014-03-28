#!/usr/bin/python

# -------------------
# Background Information
#
# In this problem, you will build a planner that helps a robot
# find the shortest way in a warehouse filled with boxes
# that he has to pick up and deliver to a drop zone.
#For example:
#
#warehouse = [[ 1, 2, 3],
#             [ 0, 0, 0],
#             [ 0, 0, 0]]
#dropzone = [2,0] 
#todo = [2, 1]
# Robot starts at the dropzone.
# Dropzone can be in any free corner of the warehouse map.
# todo is a list of boxes to be picked up and delivered to dropzone. 
# Robot can move diagonally, but the cost of diagonal move is 1.5 
# Cost of moving one step horizontally or vertically is 1.0
# If the dropzone is at [2, 0], the cost to deliver box number 2
# would be 5.

# To pick up a box, robot has to move in the same cell with the box.
# When a robot picks up a box, that cell becomes passable (marked 0)
# Robot can pick up only one box at a time and once picked up 
# he has to return it to the dropzone by moving on to the cell.
# Once the robot has stepped on the dropzone, his box is taken away
# and he is free to continue with his todo list.
# Tasks must be executed in the order that they are given in the todo.
# You may assume that in all warehouse maps all boxes are
# reachable from beginning (robot is not boxed in).

# -------------------
# User Instructions
#
# Design a planner (any kind you like, so long as it works).
# This planner should be a function named plan() that takes
# as input three parameters: warehouse, dropzone and todo. 
# See parameter info below.
#
# Your function should RETURN the final, accumulated cost to do
# all tasks in the todo list in the given order and this cost
# must which should match with our answer).
# You may include print statements to show the optimum path,
# but that will have no effect on grading.
#
# Your solution must work for a variety of warehouse layouts and
# any length of todo list.
# Add your code at line 76.
# 
# --------------------
# Parameter Info
#
# warehouse - a grid of values. where 0 means that the cell is passable,
# and a number between 1 and 99 shows where the boxes are.
# dropzone - determines robots start location and place to return boxes 
# todo - list of tasks, containing box numbers that have to be picked up
#
# --------------------
# Testing
#
# You may use our test function below, solution_check
# to test your code for a variety of input parameters. 

warehouse = [[ 1, 2, 3],
             [ 0, 0, 0],
             [ 0, 0, 0]]
dropzone = [2,0] 
todo = [2, 1]

# ------------------------------------------
# plan - Returns cost to take all boxes in the todo list to dropzone
#
# ----------------------------------------
# modify code below
# ----------------------------------------

def expandPoint(point, oList, eList, warehouse, goalVal):
	g = point[0]
	r = point[1][0]
	c = point[1][1]
	rcount = len(warehouse)
	ccount = len(warehouse[0])
	#print "doing point " + str(r) + ", " + str(c)
	for i in range(-1,2):
		for j in range(-1,2):
			eRow = r + i
			eCol = c + j
			#print  "\texpanding " + str(i) + ", " + str(j) + " for new vals of " + str(eRow) + ", " + str(eCol)

			
			if eRow < 0 or eCol < 0:
				continue
			
			if eRow > rcount-1 or eCol > ccount-1:
				#print "\t\ttoo large " + str(r) + " & " + str(c)
				continue
			
			if warehouse[eRow][eCol] > 0 and warehouse[eRow][eCol] != goalVal:
				#print "Can't go do " + str(eRow) + ", " + str(eCol) + " because i thas another box"
				continue
				
			if [eRow, eCol] not in eList:
			
				
				newG = g
				if abs(i) + abs(j) == 2:
					newG = g + 1.5
				else:
					newG = g + 1.0
				
				#print "\t\tAdding " + str(eRow) + ", " + str(eCol)
				eList.append([eRow, eCol])
				oList.append([(newG), [eRow, eCol]])
			
def plan(warehouse, dropzone, todo):
	costsum = 0
	
	#print "Dropzone is " + str(dropzone[0]) + ", " + str(dropzone[1])
	
	#for i in range(len(warehouse)):
		#print warehouse[i]
	
	#print "****"
	#print "TODO: " 
	#for i in range(len(todo)):
	#	print todo[i]
		
	#print "****"
	foundCount = 0
	thisGoal = todo[foundCount]

	#print "First goal is " + str(thisGoal)
	
	found = False
	
	expandedList = []
	
	open = []
	open.append([0, dropzone])
	expandedList.append(open[0][1])
	
	
	while found == False:
	
		#print "iteration"
		open.sort()
		open.reverse()
		#print "\n\n\n*****"
		#print open
		#print "****"
		thisPoint = open.pop()
		#print "popped " + str(thisPoint[1][0]) + ", " + str(thisPoint[1][1])

		if warehouse[thisPoint[1][0]][thisPoint[1][1]] == thisGoal:
			#print "weeee found " + str(thisGoal) + " with a cost of " + str(thisPoint[0])
			warehouse[thisPoint[1][0]][thisPoint[1][1]] = 0
			costsum += thisPoint[0]
			foundCount += 1
			if foundCount >= (len(todo)):
				#print "we good yall found dem all"
			
				found = True
			else:
				open = []
				expandedList = []
				open.append([0, dropzone])
				expandedList.append(open[0][1])
				thisGoal = todo[foundCount]
				continue
				
		# expand the next one
		expandPoint(thisPoint, open, expandedList, warehouse, thisGoal)
		
	
		#print "********"
		#open.sort()


	#print "SUM: " + str(costsum)
	return (costsum * 2)
    
################# TESTING ##################
       
# ------------------------------------------
# solution check - Checks your plan function using
# data from list called test[]. Uncomment the call
# to solution_check to test your code.
#
def solution_check(test, epsilon = 0.00001):
    answer_list = []
    
    import time
    start = time.clock()
    correct_answers = 0
    for i in range(len(test[0])):
        user_cost = plan(test[0][i], test[1][i], test[2][i])
        true_cost = test[3][i]
        if abs(user_cost - true_cost) < epsilon:
            print "\nTest case", i+1, "passed!"
            answer_list.append(1)
            correct_answers += 1
            #print "#############################################"
        else:
            print "\nTest case ", i+1, "unsuccessful. Your answer ", user_cost, "was not within ", epsilon, "of ", true_cost 
            answer_list.append(0)
    runtime =  time.clock() - start
    if runtime > 1:
        print "Your code is too slow, try to optimize it! Running time was: ", runtime
        return False
    if correct_answers == len(answer_list):
        print "\nYou passed all test cases!"
        return True
    else:
        print "\nYou passed", correct_answers, "of", len(answer_list), "test cases. Try to get them all!"
        return False
#Testing environment
# Test Case 1 
warehouse1 = [[ 1, 2, 3],
             [ 0, 0, 0],
             [ 0, 0, 0]]
dropzone1 = [2,0] 
todo1 = [2, 1]
true_cost1 = 9


#res = plan(warehouse1, dropzone1, todo1)

# Test Case 2
warehouse2 = [[   1, 2, 3, 4],
             [   0, 0, 0, 0],
             [   5, 6, 7, 0],
             [ 'x', 0, 0, 8]] 
dropzone2 = [3,0] 
todo2 = [2, 5, 1]
true_cost2 = 21
res = plan(warehouse2, dropzone2, todo2)
# Test Case 3
warehouse3 = [[  1, 2, 3, 4, 5, 6, 7],
             [   0, 0, 0, 0, 0, 0, 0],
             [   8, 9,10,11, 0, 0, 0],
             [ 'x', 0, 0, 0,  0, 0, 12]] 
dropzone3 = [3,0] 
todo3 = [5, 10]
true_cost3 = 18

# Test Case 4
warehouse4 = [[  1,17, 5,18, 9,19, 13],
             [   2, 0, 6, 0,10, 0, 14],
             [   3, 0, 7, 0,11, 0, 15],
             [   4, 0, 8, 0,12, 0, 16],
             [   0, 0, 0, 0, 0, 0, 'x']] 
dropzone4 = [4,6] 
todo4 = [13, 11, 6, 17]
true_cost4 = 41

#testing_suite = [[warehouse1, warehouse2, warehouse3, warehouse4],
#                 [dropzone1, dropzone2, dropzone3, dropzone4],
#                 [todo1, todo2, todo3, todo4],
#                 [true_cost1, true_cost2, true_cost3, true_cost4]]


#solution_check(testing_suite) #UNCOMMENT THIS LINE TO TEST YOUR CODE

