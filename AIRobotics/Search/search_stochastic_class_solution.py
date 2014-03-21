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

success_prob = 0.5                      
failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
collision_cost = 1000                    
cost_step = 1        
              
# ----------------------------------------
# modify code below
# ----------------------------------------
def isValidCell(r, c):
	if r < 0 or c < 0:
		return False
	if r >= len(grid) or c >= len(grid[0]):
		return False
		
	return True
	
def optimum_policy():
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    print "Rows = " + str(len(grid))
    print "Cols = " + str(len(grid[0]))
    
    change = True

    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0

                        change = True

                elif grid[x][y] == 0:
					v2 = cost_step
					
					for a in range(len(delta)):
						print "Updating cost for direction " + str(x) + ", " + str(y) + " direction " + delta_name[a]
						deltaIndex = a 
						# forward
						x2 = x + delta[deltaIndex][0]
						y2 = y + delta[deltaIndex][1]
						print "new point " + str(x2) + ", " + str(y2)
						if isValidCell(x2, y2) and grid[x2][y2] == 0:
							v2 = v2 + (  success_prob * value[x2][y2] )
						else:
							v2 = v2 + ( ( 1- success_prob) * 1000 )
						
						# left
						deltaIndex = (a+1)% len(delta)
						print "delta for left turn is " + str(deltaIndex)
						x2 = x + delta[deltaIndex][0]
						y2 = y + delta[deltaIndex][1]
						if isValidCell(x2, y2) and grid[x2][y2] == 0:
							v2 = v2 + (  success_prob * value[x2][y2] )
						else:
							v2 = v2 + ( ( 1- success_prob) * 1000 )
							
						# riht
						deltaIndex = (a-1)%len(delta)
						print "delta index for right turn is " + str(deltaIndex)
						x2 = x + delta[deltaIndex][0]
						y2 = y + delta[deltaIndex][1]
						if isValidCell(x2, y2) and grid[x2][y2] == 0:
							v2 = v2 + (  success_prob * value[x2][y2] )
						else:
							v2 = v2 + ( ( 1- success_prob) * 1000 )
									
						if v2 < value[x][y]:
							change = True
							value[x][y] = v2
							policy[x][y] = delta_name[a]

    
    policy = value
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
