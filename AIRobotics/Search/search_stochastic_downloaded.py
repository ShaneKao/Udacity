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
success_prob = 0.5                      
failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
collision_cost = 100                 
cost_step = 1

def get_value(n, value):
    if not (0 <= n[0] and n[0] < len(grid) and 0 <= n[1] and n[1] < len(grid[0])) or value[n[0]][n[1]] == 1000:
        return collision_cost
    else:
        return value[n[0]][n[1]]

def awesome(value):
    value[goal[0]][goal[1]] = 0

    open = [goal]
    closed = []

    while len(open) > 0:
        next = open.pop()

        neighbors = []
        deltas = []
        for d in delta:
            n = [ d[0] + next[0], d[1] + next[1] ]
            if 0 <= n[0] and n[0] < len(grid):
                if 0 <= n[1] and n[1] < len(grid[0]):
                    if grid[n[0]][n[1]] == 0:
                        neighbors.append(n)
                        deltas.append(d)

        for i in range(len(neighbors)):
            n = neighbors[i]
            d = deltas[i]
            if value[n[0]][n[1]] == 1000: #if untouched, extra safety
                forward = get_value([n[0] + d[0], n[1] + d[1]], value)
                ld = delta[delta.index(d)+1] # +1i, leftdelta
                print ld
                rd = delta[delta.index(d)-1]# -1i, rightdelta
                left = get_value([n[0] + ld[0], n[1] + ld[1]], value)
                right = get_value([n[0] + rd[0], n[1] + rd[1]], value)
                value[n[0]][n[1]] = failure_prob * left + failure_prob * right + success_prob * forward + cost_step

        for n in neighbors:
            if not n in closed:
                open.append(n)

        print open

        closed.append(next)
    return value

def stochastic_value():    
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    for x in range(1000):
        print value
        value = awesome(value)
    #Done!
    for row in value:
        print row

    #Next, find path
    for row in range(len(grid)):
        for item in range(len(grid[0])):
            next = [row, item]
            neighbors = []
            costs = []
            for d in delta:
                n = [ d[0] + next[0], d[1] + next[1] ]
                if 0 <= n[0] and n[0] < len(grid):
                    if 0 <= n[1] and n[1] < len(grid[0]):
                        if grid[n[0]][n[1]] == 0:
                            neighbors.append(n)
                            costs.append(value[n[0]][n[1]])

            p = neighbors[costs.index(min(costs))]
            d = [p[0] - next[0], p[1] - next[1]]
            character = delta_name[delta.index(d)]
            if value[next[0]][next[1]] != 1000:
                policy[next[0]][next[1]] = character

    policy[goal[0]][goal[1]] = '*'

    for row in policy:
        print row
    return value, policy

stochastic_value()