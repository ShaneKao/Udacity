#!/usr/bin/python

# Write a program that will iteratively update and
# predict based on the location measurements 
# and inferred motions shown below. 

def update(mean1, var1, mean2, var2):
	print "var 1 = " + str(var1) + " var2 = " + str(var2)
	new_mean = (var2 * mean1 + var1 * mean2) / (var1 + var2)
	new_var = 1/(1/var1 + 1/var2)
	return [new_mean, new_var]

def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0
sig = 10000

#Please print out ONLY the final values of the mean
#and the variance in a list [mu, sig]. 

running = [mu, sig]
# Insert code here
for i in range(len(measurements)):
  # measure
  running = update(running[0], running[1], measurements[i], measurement_sig)
  # predict where we will be after mooving next
  running = predict(running[0], running[1], motion[i], motion_sig)
  mu = running[0]
  sig = running[1]
  
print [mu, sig]
