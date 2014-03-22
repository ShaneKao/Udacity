#!/usr/bin/python


# -----------
# User Instructions
#
# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth)
# and returns a smooth path.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached. The update should be done according to the
# gradient descent equations given in the previous video:
#
# If your function isn't submitting it is possible that the
# runtime is too long. Try sacrificing accuracy for speed.
# -----------


from math import *

# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

# ------------------------------------------------
# smooth coordinates
#

def smooth(path, weight_data = 0.5, weight_smooth = 0.1):

    # Make a deep copy of path into newpath
    newpath = [[0 for col in range(len(path[0]))] for row in range(len(path))]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] = path[i][j]

	p2 = [[0 for col in range(len(path[0]))] for row in range(len(path))]

	for i in range(len(path)):
		for j in range(len(path[0])):
			p2[i][j] = path[i][j]
	


	
    #### ENTER CODE BELOW THIS LINE ###
	newpath[0] = path[0]
	newpath[len(path)-1] = path[len(path) - 1]
	#print newpath
	
	delta = tolerance
	#for r in range(15):
	while delta >= tolerance:
		delta = 0
		#print "using r=" + str(r) + " path is " + str(len(path))
		for i in range(1, (len(path) - 1)):
			auxx = newpath[i][0]
			auxy = newpath[i][1]
			#print "Smoothing for point " + str(path[i][0]) + ", " + str(path[i][1]) + " max delta = " + str(delta)
			x1 = newpath[i][0] + (weight_data * (path[i][0] - newpath[i][0]))
			#print "updated x1 to " + str(x1)
			x2 = x1 + (weight_smooth * ( newpath[i+1][0] + newpath[i-1][0] - 2 * x1 ))
			#print "updated x2 to " + str(x2)
			
			if newpath[i][0] < delta and x2 > 0:
				delta = x2
				
			newpath[i][0] = x2
			
			
			y1 = newpath[i][1] + weight_data * (path[i][1] - newpath[i][1])
			##print "updated x1 to " + str(x1)
			y2 = y1 + (weight_smooth * ( newpath[i+1][1] + newpath[i-1][1] - 2 * y1 ))
			##print "updated x2 to " + str(x2)
			newpath[i][1] = y2
			
			delta += abs(auxx - x2)
			delta += abs(auxy - y2)
	
	
	return newpath # Leave this line for the grader!

tolerance = .00001
# feel free to leave this and the following lines if you want to print.
newpath = smooth(path)

# thank you - EnTerr - for posting this on our discussion forum
for i in range(len(path)):
    print '['+ ', '.join('%.3f'%x for x in path[i]) +'] -> ['+ ', '.join('%.3f'%x for x in newpath[i]) +']'









