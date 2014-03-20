#!/usr/bin/python

# ----------
# User Instructions:
# 
# Create a function optimum_policy() that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell.
# 
# un-navigable cells must contain an empty string
# WITH a space, as shown in the previous video.
# Don't forget to mark the goal with a '*'

# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy():
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    change = True

    while change:
        change = False

		# set the values of the cells
		# 
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0

                        change = True

                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            v2 = value[x2][y2] + cost_step

                            if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2
    
    policy = value
    for i in range(len(value)):
		print value[i]
		
    for i in range(len(policy)):
        for j in range(len(policy[i])):
            
            if policy[i][j] == 99:
                policy[i][j] = ' '
                continue
            
            if i == goal[0] and j == goal[1]:
                policy[i][j] = '*'
                continue
                
            bestcost = 99
            bestIndex = -1
            
            for k in range(len(delta)):
                x2 = i + delta[k][0]
                y2 = j + delta[k][1]
                if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                    #print "checking neighbor " + str(x2) + ", " + str(y2)
                    if value[x2][y2] < bestcost:
                        bestcost = value[x2][y2]
                        bestIndex = k
                    
            policy[i][j] = delta_name[bestIndex]   
            #print "For point " + str(i) + ", " + str(k) + " the best cost is " + str(bestcost) + " delta index is " + str(bestIndex)
            
         
    
    return policy # Make sure your function returns the expected grid.


pp = optimum_policy()
for i in range(len(pp)):
    print pp[i]
