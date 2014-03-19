#!/usr/bin/python

# ----------
# User Instructions:
# 
# Create a function compute_value() which returns
# a grid of values. Value is defined as the minimum
# number of moves required to get from a cell to the
# goal. 
#
# If it is impossible to reach the goal from a cell
# you should assign that cell a value of 99.

# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# insert code below
# ----------------------------------------

def search(point):
    open = []
    
    if grid[point[0]][point[1]] == 1:
        #print "Block cell at point " + str(point[0]) + ", " + str(point[1])
        return 99
    
    open.append([0, point[0], point[1]])
    found = False
    terminate = False
    
    expandedList = []

    while found == False and terminate == False:
        if [goal[0], goal[1]] in expandedList:
            node = open[len(open)-1]
            thiscost = node[0]
            #print "Found that thang for point " + str(point[0]) + ", " + str(point[1]) + " cost = " + str(thiscost)
            #print open
            found = True
            return thiscost
            break
                
        if len(open) == 0:
            #print "TERMINATE"
            return 99
        
            terminate = True
        else:
            open.sort()
            #print "sorted"
            
            #for k in range(len(open)):
            #    print open[k]
                    
            expanded = open.pop()
            
            x = expanded[1]
            y = expanded[2]
            g = expanded[0]
            
            for i in range(len(delta)):
                   x2 = x + delta[i][0]
                   y2 = y + delta[i][1]
                
                   
                        
                   if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        g2 = g + cost
                        newpoint = [x2, y2]
                        if grid[x2][y2] == 1:
                            continue
                        
                        if newpoint not in expandedList:
                            #print "adding " + str(x2) + ", " + str(y2)
                            expandedList.append([x2, y2])
                            open.append([ g2, x2, y2])
   
    
    return -1

def compute_value():
    value = [[-2 for row in range(len(grid[0]))] for col in range(len(grid))]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if goal[0] == i and goal[1] == j:
                value[i][j] = 0
            else:
                value[i][j] = search([i,j])
            
    return value #make sure your function returns a grid of values as demonstrated in the previous video.



val =  compute_value()
for i in range(len(val)):
    print val[i]
