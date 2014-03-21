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

#grid = [[0, 1, 0],
#        [0, 0, 0]]
goal = [0, len(grid[0])-1] # Goal is in top right corner


delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

success_prob = 1                    
failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
collision_cost = 100                    
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
	
def stochastic_value():
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    change = True
    for f in range(1):
			while change:
				#print "***Iteration"
				change = False
				for x in range(len(grid)):
					for y in range(len(grid[x])):
						#print "updating " + str(x) + ", " + str(y)
						if goal[0] == x and goal[1] == y:
							if value[x][y] > 0:
								value[x][y] = 0
			
								change = True
			
						elif grid[x][y] == 0:
							#print "\t going to try to update it"
							for a in range(len(delta)):
								v2 = cost_step

								#print "Updating cost for direction " + str(x) + ", " + str(y) + " direction " + delta_name[a]
								deltaIndex = a 
								# forward
								x2 = x + delta[deltaIndex][0]
								y2 = y + delta[deltaIndex][1]
								#print "new point " + str(x2) + ", " + str(y2)
								if isValidCell(x2, y2) and grid[x2][y2] == 0:
									#print "adding " + str(v2) + " plus " + str(cost_step)
									v2 = v2 + ( success_prob * value[x2][y2])
								else:
									v2 = v2 + ( success_prob * collision_cost)
								
								#print "\tforward v is " + str(v2)
								# left
								deltaIndex = (a+1)% len(delta)
								#print "delta for left turn is " + str(deltaIndex)
								x2 = x + delta[deltaIndex][0]
								y2 = y + delta[deltaIndex][1]
								if isValidCell(x2, y2) and grid[x2][y2] == 0:
									v2 = v2 + (  failure_prob * value[x2][y2] )
								else:
									v2 = v2 + ( failure_prob * collision_cost )
									
								# riht
								deltaIndex = (a-1)%len(delta)
								#print "delta index for right turn is " + str(deltaIndex)
								x2 = x + delta[deltaIndex][0]
								y2 = y + delta[deltaIndex][1]
								if isValidCell(x2, y2) and grid[x2][y2] == 0:
									v2 = v2 + (  failure_prob * value[x2][y2] )
								else:
									v2 = v2 + ( failure_prob * collision_cost )
								
								#print "\tnew cost is " + str(v2)
								if v2 < value[x][y]:
									#print "updating cost of " + str(x) + ", " + str(y) + " to " + str(v2)
									#print "Index for cost " + str(v2) + " is " + str(a)
									change = True
									value[x][y] = v2
									policy[x][y] = delta_name[a]
				
  
    
    return value, policy # Make sure your function returns the expected grid.


pp = stochastic_value()
vals = pp[0]
for i in range(len(vals)):
	print vals[i]
pol = pp[1]
for i in range(len(pol)):
	print pol[i]
