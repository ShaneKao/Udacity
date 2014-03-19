#!/usr/bin/python
# -----------
# User Instructions:
#
# Modify the the search function so that it returns
# a shortest path as follows:
# 
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left, 
# up, and down motions. NOTE: the 'v' should be 
# lowercase.
#
# Your function should be able to do this for any
# provided grid, not just the sample grid below.
# ----------


# Sample Test case
#grid = [[0, 0, 1, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0],
##        [0, 0, 1, 0, 1, 0],
#        [0, 0, 1, 0, 1, 0],
#        [0, 0, 1, 0, 1, 0]]

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

# ----------------------------------------
# modify code below
# ----------------------------------------

def search():
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    costs = []
    expand = []
    for i in range(len(grid)):
        newrow = []
        for j in range(len(grid[i])):
            newrow.append(-1)
        
        expand.append(newrow)    
    
    for i in range(len(grid)):
        newrow = []
        for j in range(len(grid[i])):
            newrow.append(-1)
        
        costs.append(newrow)
        
	
    x = init[0]
    y = init[1]
    g = 0

    open = [[g, x, y]]
    costs[x][y] = g
    found = False  # flag that is set when search is complet
    resign = False # flag set if we can't find expand
    ecount = 0
    while not found and not resign:
        if len(open) == 0:
            resign = True
            return 'fail'
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]
            expand[x][y] = ecount
            ecount = ecount + 1
            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            open.append([g2, x2, y2])
                            costs[x2][y2] = g2
                            closed[x2][y2] = 1
         

	
    steps = []
    for i in range(len(grid)):
        newrow = []
        for j in range(len(grid[i])):
            newrow.append(' ')
        
        steps.append(newrow)
	
    steps[goal[0]][goal[1]] = '*'
    
    done = False
    
    curX = goal[0]
    curY = goal[1]
    
    while not done:
        neighborCost = []
        minCost = -1
        directionIndex = -1
        bestX = -1
        bestY = -1
        
        for j in range(len(delta)):
            newX = curX + delta[j][0]
            newY = curY + delta[j][1]
            if newX >= 0 and newX < len(grid) and newY >=0 and newY < len(grid[0]):
                if minCost == -1 or costs[newX][newY] < minCost and costs[newX][newY] != -1:
                    #print "setting minst " + str(newX) + "-" + str(newY) + " to " + str(costs[newX][newY])
                    minCost = costs[newX][newY]
                    directionIndex = j
                    #print "setting direction index to " + str(j)
                    bestX = newX
                    bestY = newY
                 
        curX = bestX
        curY = bestY
        
        directionIndex = (directionIndex + 2) % len(delta_name)
        steps[bestX][bestY] = delta_name[directionIndex]
        #print "Current is now " + str(curX) + ", " + str(curY)
        if curX == init[0] and curY == init[1]:
            
            done = True
        
    for i in range(len(steps)):
		print steps[i]
	
    expand = steps
    return expand
    #print "****"
    #for i in range(len(expand)):
        #print expand[i]


search()

