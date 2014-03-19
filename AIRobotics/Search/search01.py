#!/usr/bin/python


# ----------
# User Instructions:
# 
# Define a function, search() that takes no input
# and returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space
def findLowestCost(openList):
	lowestIndex = 0
	for i in range(len(openList)):
		#print "Looking up Cost " + str(openList[i][0])
		if openList[i] < openList[lowestIndex]:
			lowestIndex = i
	
	return lowestIndex

def isGoal(point):
	if ( point[0] == 4 and point[1] == 5):
		return True;
	
	return False;

def expandCells(openList):

	lowestIndex = findLowestCost(openList)
	#print "     Lowest index is " + str(lowestIndex) + " total len is " + str(len(openList))
	#print "**************"
	#print "****Expanding point " + str(openList[lowestIndex][1]) + ", " + str(openList[lowestIndex][2])
	
	# [r, c]
	expandingPoint = [ openList[lowestIndex][1], openList[lowestIndex][2]]
	checked[openList[lowestIndex][1]][openList[lowestIndex][2]] = True
	

	currentOpen = openList
	oldPoint = openList[lowestIndex]
	expandedList.append(oldPoint)

	currentG = openList[lowestIndex][0] + cost
	#print "Current G is " + str(newG)
	currentOpen.pop(lowestIndex)
	 
	for i in range(len(delta)):
	
		newpoint = [ (oldPoint[1] + delta[i][0]),  (oldPoint[2] + delta[i][1])]

		if isValidCell(newpoint):
			currentOpen.append([currentG, newpoint[0], newpoint[1]])
			
		
	return currentOpen

	
	
currentG = 0

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 1, 0, 1, 0]]

checked = []
for i in range(len(grid)):
	checkedrow = []
	for j in range(len(grid[i])):
		checkedrow.append(False)
	

	checked.append(checkedrow)
	
def isValidCell(point):
	
	# point[0] = row
	
		
	if point[0] < 0:
		return False
	# check row too high
	if point[0] >= len(grid):
		return False
	# check col too smal
	if point[1] < 0:
		return False
	# check col too high
	if point[1] >= len(grid[0]):
		return False
	
	if grid[point[0]][point[1]] == 1:
		return False;

	
	#print "looking up values " + str(point[0]) + ", " + str(point[1])
	if checked[point[0]][point[1]]:
		#print "Already been checked bro"
		return False;

		
	return True;
	
init = [0, 0]

goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']
cost = 1


def search():
# ----------------------------------------
# insert code here and make sure it returns the appropriate result
# ----------------------------------------
	open =  [ [ 0, init[0], init[1] ] ]
	keepLooping = True
	path = []
	while keepLooping == True:
		open = expandCells(open)
		#print "checking " + str(goal[1]) + "," + str(goal[0])
		if checked[goal[0]][goal[1]] == True:
			keepLooping = False
			node = expandedList[len(expandedList) - 1]
			path =  node
			return path
		if len(open) == 0:
			path = open
			keepLooping = False
			return 'fail'




expandedList = []
openList = [ [ 0, init[0], init[1] ] ]

print search()
