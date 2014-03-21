#!/usr/bin/python
# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# takes no input and RETURNS two grids. The
# first grid, value, should contain the computed
# value of each cell as shown in the video. The
# second grid, policy, should contain the optimum
# policy for each cell.
#
# Stay tuned for a homework help video! This should
# be available by Thursday and will be visible
# in the course content tab.
#
# Good luck! Keep learning!
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.
#
# NOTE: Please do not modify the values of grid,
# success_prob, collision_cost, or cost_step inside
# your function. Doing so could result in your
# submission being inappropriately marked as incorrect.

# -------------
# GLOBAL VARIABLES
#
# You may modify these variables for testing
# purposes, but you should only modify them here.
# Do NOT modify them inside your stochastic_value
# function.

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
   
goal = [0, len(grid[0])-1] # Goal is in top right corner


delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

success_prob = 1.0                      
failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
collision_cost = 1000                    
cost_step = 1        
                     

############## INSERT/MODIFY YOUR CODE BELOW ##################
#
# You may modify the code below if you want, but remember that
# your function must...
#
# 1) ...be called stochastic_value().
# 2) ...NOT take any arguments.
# 3) ...return two grids: FIRST value and THEN policy.
def isValid(point, visited=[]):
	
	#print "Is point " + str(point[0]) + ", " + str(point[1]) + " valid"
	r = point[0]
	c = point[1]
	if r < 0 or r >= len(grid):
		#print "OOB " + str(r) + ", " + str(c)
		return False
	if c < 0 or c >=len(grid[0]):
		#print "OOB" + str(r) + ", " + str(c)
		return False
		
	if grid[r][c] == 1:
		#print "blocked"
		return False
	
	if [r,c] in visited:
		#print "already visited " + str(r) + ", " + str(c)
		return False
	#print "point " + str(r) + ", " + str(c) + " is valid"

	return True
		

def addNeighbors(point, open, visited):
	g = point[0]
	r = point[1] 
	c = point[2]

	for i in range(len(delta)):
		# for each direction, find forward, left and right.
		
		r2 = r + delta[i][0]
		c2 = r + delta[1][1]
		newCost = g + ( success_prob * 
		
		
		
		#if isValid([r2, c2], visited):
		#	open.append([(g+cost_step), r2, c2])
		#	visited.append([r,c])
		
			
def search(point, value):
	oldpoint = point
	init = point
	open = []
	visited = []
	open.append([0, point[0], point[1]])
	keepLooping = True
	
	if grid[point[0]][point[1]] == 1:
		return 1000
		
	while keepLooping == True:
		#print "***********************************"
		#print "Open len is " + str(len(open))
		if len(open) == 0:
			print "Empty"
			return 1000
			break
		
		
		open.sort()
		open.reverse()
		#print "*** before sort"
		#print open
		p = open.pop()
		#print "***** after pop"
		#print open
		g = p[0]
		r = p[1]
		c = p[2]
		
		if r == goal[0] and c == goal[1]:
			#print "GOAAAAL for point " + str(oldpoint[0]) + ", " + str(oldpoint[1]) + str(g)
			keepLooping = False
			return g
		else:
			addNeighbors(p, open, visited)
			#print "*** after neightbors"
			#print open
			
def findStep(point, values):
	r = point[0] 
	c = point[1]
	lowindex = 70
	lowvalue = 9999
	if grid[point[0]][point[1]] == 1:
		return ' '
	
	if point[0] == goal[0] and point[1] == goal[1]:
		return "*"
		
	for i in range(len(delta)):
		r2 = r + delta[i][0]
		c2 = c + delta[i][1]
		if not isValid([r2, c2]):
			continue
			
		if values[r2][c2] < lowvalue:
			#print "Value " + str(values[r2][c2]) + " was lower on spot " + str(r2) + ", " + str(c2)

			lowvalue = values[r2][c2]
			lowindex = i
	
	#print "Low index is " + str(lowindex)
	return delta_name[lowindex]

#def findUpdatedStep(r, c values):
#	r = point[0] 
#	c = point[1]
#	lowindex = 70
#	lowvalue = 9999
#	if grid[point[0]][point[1]] == 1:
#		return ' '
#	
#	if point[0] == goal[0] and point[1] == goal[1]:
#		return "*"
#		
#	for i in range(len(delta)):
#		r2 = r + delta[i][0]
#		c2 = c + delta[i][1]
#		if not isValid([r2, c2]):
#			continue
#			
#		if values[r2][c2] < lowvalue:
#			#print "Value " + str(values[r2][c2]) + " was lower on spot " + str(r2) + ", " + str(c2)
#
#			lowvalue = values[r2][c2]
#			lowindex = i
#	
#	#print "Low index is " + str(lowindex)
#	return delta_name[lowindex]
	
def updateValues(r, c, policy, values):
	dir = policy[r][c]
	#print "*******"
	#print "point " + str(r) + ", " + str(c)
	if values[r][c] == 0:
		#print "value is 0 returning 0"
		return 0

	if policy[r][c] == ' ':
		#print "no policy . returning the same value"
		return values[r][c]
	
	motionIndex = delta_name.index(dir)
	
	# going straight
	r2 = r + delta[motionIndex][0]
	c2 = c + delta[motionIndex][1]
	
	newcost = 0
	if isValid([r2, c2]):
		#print "checking " + str(r2) + ", " + str(c2)
		newcost = newcost + ( failure_prob * float(values[r2][c2]))
	else:
		print "forward isn't valid"
	
	#print "newcost is " + str(newcost)
	
	
	# subtrace one from the index to go left
	leftIndex = (motionIndex - 1) % 4
	r2 = r + delta[leftIndex][0]
	c2 = c + delta[leftIndex][1]
	if isValid([r2, c2]):
		#print "checking " + str(r2) + ", " + str(c2)
		newcost = newcost + ( failure_prob * values[r2][c2])
	else:
		newcost = newcost + ( failure_prob * 100)
		
	# add one to the index to go right
	rightIndex = (motionIndex + 1 ) % 4
	r2 = r + delta[rightIndex][0]
	c2 = c + delta[rightIndex][1]
	if isValid([r2, c2]):
		#print "checking " + str(r2) + ", " + str(c2)
		newcost = newcost + ( failure_prob * values[r2][c2])
	else:
		newcost = newcost + ( failure_prob * 100)
		
	#print "Updating value for point " + str(r) + ", " + str(c) + " with direction " + dir + " dir name index = " + str(motionIndex) + " cost " + str(newcost)
	return newcost

def stochastic_value():
	value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
	policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
	#value[3][1] = search([3,1], value)

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			value[i][j] = search([i,j], value)
			
	#for i in range(len(grid)):
	#	for j in range(len(grid)):
	#		policy[i][j] = findStep([i, j], value)
	
	thesevalues = []
	#for n in range(1):
	#	thesevalues = value
	#	for i in range(len(grid)):
	#		for j in range(len(grid[i])):
	#			value[i][j] = updateValues(i, j, policy, thesevalues )
	#	
	#	print "finding next step for 1,3"
	#	val = findStep([1, 3], value)
	#	print "value is " + str(val)
	#	#for i in range(len(grid)):
	#	#	for j in range(len(grid)):
	#	#		policy[i][j] = findStep([i, j], value)
	#	#
	#	#print "\n\n**** updated policy ****"
	#	#for i in range(len(policy)):
	#	#	print policy[i]
	#	#
	#	#print "*********"
	#value = thesevalues
	return value, policy

#search([0,0], value]
val = stochastic_value()
for i in range(len(val[0])):
	print val[0][i]
	
for i in range(len(val[1])):
	print val[1][i]
