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

grid = [[0, 1, 0],
        [0, 0, 0]]
		
goal = [0, len(grid[0])-1] # Goal is in top right corner


delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

success_prob = 0.5                      
failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
collision_cost = 100                    
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
		
def isCollision(r, c):
	r = point[0]
	c = point[1]
	if r < 0 or r >= len(grid):
		#print "OOB " + str(r) + ", " + str(c)
		return True
	if c < 0 or c >=len(grid[0]):
		#print "OOB" + str(r) + ", " + str(c)
		return True
	
	if grid[r][c] == 1:
		return True;
		
	return False
	
def addNeighbors(point, open, visited):
	g = point[0]
	r = point[1] 
	c = point[2]

	for i in range(len(delta)):
		r2 = r + delta[i][0]
		c2 = c + delta[i][1]
		if isValid([r2, c2], visited):
			newcost = (cost_step + g) *  success_prob
			open.append([(g+cost_step), r2, c2])
			visited.append([r,c])

def isValidCell(r, c):
	if r < 0 or r >= len(grid):
		#print "OOB " + str(r) + ", " + str(c)
		return False
	if c < 0 or c >=len(grid[0]):
		#print "OOB" + str(r) + ", " + str(c)
		return False
		
	if grid[r][c] == 1:
		#print "blocked"
		return False

	return True
	

def search( value):
	
	value[goal[0]][goal[1]] = 0
	updatedValues = value
	for a in range(len(grid)):
		for b in range(len(grid[a])):
			#print "****** New point " + str(a) + ", " + str(b)
			r = a
			c = b
			if goal[0] == r and goal[1] == c:
				updatedValues[r][c] = 0
				continue
			
			if grid[r][c] == 1:
				#print "val was 1 for " + str(a) + ", " + str(b)
				updatedValues[r][c] = collision_cost
				continue
				
			for i in range(4):
				#print "checking delta for direction " + delta_name[i] + " for point " + str(a) + ", " + str(b)
				# checking forward
				r2 = r + delta[i][0]
				c2 = r + delta[i][1]
				newcost = value[r][c]
				if isValidCell(r2, c2):
					newcost = newcost + ( .5 * value[r2][c2])
				else:
					newcost = newcost + (.5 * collision_cost )
					
				# checking left
				newIndex = (i + 1) % len(delta)
				#print"new index is " + str(newIndex)
				r2 = r + delta[newIndex][0]
				c2 = r + delta[newIndex][1]
				if isValidCell(r2, c2):
					newcost = newcost + ( .25 * value[r2][c2])
				else:
					newcost = newcost + ( .25 * collision_cost)
					
				#print "left cell is " + str(r2) + ", " + str(c2)
				
				# checking right
				newIndex = (i - 1) % len(delta)
				#print"new index is " + str(newIndex)
				r2 = r + delta[newIndex][0]
				c2 = r + delta[newIndex][1]
				if isValidCell(r2, c2):
					newcost = newcost + ( .25 * value[r2][c2])
				else:
					newcost = newcost + ( .25 * collision_cost)
		
				#print "right cell is " + str(r2) + ", " + str(c2)
				print "newcost = " + str(newcost) + " for point " + str(a) + ", " + str(b)

				if newcost < value[r][c] or value[r][c] == 0:
					updatedValues[r][c] = newcost
					
	value = updatedValues		
	
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

	
def updateValues(r, c, policy, values):
	dir = policy[r][c]
	
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
			if grid[i][j] == 0:
				value[i][j] = 0
			
	for i in range(1):
		search( value)
	
	return value, policy

#search([0,0], value]
val = stochastic_value()
for i in range(len(val[0])):
	print val[0][i]
	
for i in range(len(val[1])):
	print val[1][i]
