#!/usr/bin/python
# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D() below.
#
# You are given a car in a grid with initial state
# init = [x-position, y-position, orientation]
# where x/y-position is its position in a given
# grid and orientation is 0-3 corresponding to 'up',
# 'left', 'down' or 'right'.
#
# Your task is to compute and return the car's optimal
# path to the position specified in `goal'; where
# the costs for each motion are as defined in `cost'.

# EXAMPLE INPUT:

# grid format:
#     0 = navigable space
#     1 = occupied space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 20] # the cost field has 3 values: right turn, no turn, left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D() should return the array
# 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
#
# ----------


# there are four motion directions: up/left/down/right
# increasing the index in this array corresponds to
# a left turn. Decreasing is is a right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # do right
forward_name = ['up', 'left', 'down', 'right']

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']


# ----------------------------------------
# modify code below
# ----------------------------------------
def turnLeft(point):
	r = point[0]
	c = point[1]
	o = point[2]
	newo = (o + 1) % 4
	#print "new O is " + str(newo)
	newr = point[0] + forward[newo][0]
	newc = point[1] + forward[newo][1]
	return [newr, newc, newo]

def moveForward(point):
	r = point[0]
	c = point[1]
	o = point[2]
	newo = o
	
	newr = point[0] + forward[newo][0]
	newc = point[1] + forward[newo][1]
	return [newr, newc, newo]
	
def turnRight(point):
	r = point[0]
	c = point[1]
	o = point[2]
	newo = (o - 1) % 4
	#print "new O is " + str(newo)
	newr = point[0] + forward[newo][0]
	newc = point[1] + forward[newo][1]
	return [newr, newc, newo]
	
def isValid(point):
	#print "valid for " + str(point[0]) + ", " + str(point[1])
	if point in visited:
		print "already visited"
		return False
		
	if point[0] < 0 or point[0] >= len(grid):
		return False
	if point[1] < 0 or point[1] >= len(grid[0]):
		return False
	
	if grid[point[0]][point[1]] == 1:
		#print "that cell cann't be traveled"
		return False
		
	return True

def search(point):


	open = [[0, point[0], point[1], point[2]]]
	val = grid[point[0]][point[1]]
	#print "Doing search oin point " + str(point[0]) + ", " + str(point[1]) + " with orientation " + forward_name[point[2]] + " grid val = " + str(val)
		
	
	visited = []
	if grid[point[0]][point[1]] == 1:
		#print "dude this point is a 1"
		return 999
	# 
	keepLooping = True
	while keepLooping == True:
		open.sort()
		open.reverse()
		#print open
		if len(open) == 0:
			#print "FAIL "
			return 999
			break
			
		#print open
		thispoint = open.pop()
		#print "Popped G value of " + str(thispoint[0]) + " point " + str(thispoint[1]) + ", " + str(thispoint[2])
		g = thispoint[0]
		r = thispoint[1]
		c = thispoint[2]
		o = thispoint[3]
		
		if r == goal[0] and c == goal[1]:
			keepLooping = False
			#print "GOAAAAAAAAAAAL : " + str(g)
			return g
			break
			
		forwardpoint = moveForward([r,c, o])
		#print "\t Forward point is " + str(forwardpoint[0]) + ", " + str(forwardpoint[1])
		if isValid(forwardpoint):
			#print "\tadding point as forward " + str(forwardpoint[0]) + ", " + str(forwardpoint[1])  + " with cost " + str(cost[1])
			newCost = g + cost[1]
			open.append([newCost, forwardpoint[0], forwardpoint[1], forwardpoint[2]])
			visited.append([forwardpoint[0], forwardpoint[1]])
		
		rightpoint = turnRight([r, c, o])
		
		#print "right turn"
		if isValid(rightpoint):
			#print "\t adding right point " + str(rightpoint[0]) + ", " + str(rightpoint[1]) + " with cost " + str(cost[0])
			newCost = g + cost[0]
			open.append([newCost, rightpoint[0], rightpoint[1], rightpoint[2]])
			visited.append([rightpoint[0], rightpoint[1]])
		#print rightpoint
	
		leftpoint = turnLeft([r, c, o])
		if isValid(leftpoint):
			newCost = g + cost[2]
			open.append([newCost, leftpoint[0], leftpoint[1], leftpoint[2]])
			#print "\t adding left point " + str(leftpoint[0]) + ", " + str(leftpoint[1])  + " with cost " + str(cost[2])
			visited.append([leftpoint[0], leftpoint[1]])
	

def assignValueFunction():
	

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			for k in range(4):
				val = search([i, j, k])
				#print "doing point " + str(i) + " " + str(j) + " orientation " + str(k)
				values[k][i][j] = val
				

	return values
def findBestDirectionForState(state):
	fpoint = moveForward(state)
	lpoint = turnLeft(state)
	rpoint = turnRight(state)
	
	lowestCost = 999
	rcost = 999
	lcost = 999
	fcost = 999
	#print "values " + str(forward_name[fpoint[2]]) + ", " + str(fpoint[0]) + ", " + str(fpoint[1])
	if isValid(fpoint):
		fcost = values[fpoint[2]][fpoint[0]][fpoint[1]]
	if isValid(lpoint):
		lcost = values[lpoint[2]][lpoint[0]][lpoint[1]]
	if isValid(rpoint):
		rcost = values[rpoint[2]][rpoint[0]][rpoint[1]]
	
	if fcost < lowestCost:
		lowestCost = fcost
	if lcost < lowestCost:
		lowestCost = fcost
	if rcost < lowestCost:
		lowestCost = rcost
		
	if lowestCost == fcost:
		return "#"
	if lowestCost == rcost:
		return "R"
	if lowestCost == lcost:
		return "L"
	#print "Costs are " + str(rcost) + ":" + str(fcost) + ":" + str(lcost)
	#print "got a forward point of " + str(fpoint[0]) + ", " + str(fpoint[1])
	return values[state[2]][state[0]][state[1]]
	
def optimum_policy2D():
	policy2D = [[ ' ' for row in range(len(grid[0]))] for col in range(len(grid))]
		
	myvals = assignValueFunction()
	
	#for k in range(4):
	#	print "\n\n\n******" + str(k) + " *****"
	#	v1 = myvals[k]
	#	for i in range(len(v1)):
	#		print v1[i]
	
	keepLooping = True
	
	point = init
	#print "Starting with point " + str(init[0]) + ", " + str(init[1]) + " orientation " + forward_name[init[2]]

	while keepLooping == True:
		dir = findBestDirectionForState(point)
		policy2D[point[0]][point[1]] = dir

		if dir == "#":
			point = moveForward(point)
		elif dir == "R":
			point = turnRight(point)
		elif dir == "L":
			point = turnLeft(point)
		
		if point[0] == goal[0] and point[1] == goal[1]:
			#print "GOAAAAAAAAL"
			keepLooping = False
	
	for i in range(len(policy2D)):
		print policy2D[i]
	#while keepLooping:
		
	
	return policy2D # Make sure your function returns the expected grid.

	
values = []
values.append([[999 for row in range(6)] for col in range(5)])
values.append([[999 for row in range(6)] for col in range(5)])
values.append([[999 for row in range(6)] for col in range(5)])
values.append([[999 for row in range(6)] for col in range(5)])

#print "len of values is " + str(len(values))

v1 = values[3]

loc = init
#print "initial position is "
#print loc
#print "\n\n\n"


visited = []
pol = optimum_policy2D()
#print pol
#val = search([2, 3, 0])
#print "\n\n"
#for i in range(len(pol)):
#	print pol[i]
