#!/usr/bin/python

import numpy as np

def compute_r_squared(data, predictions):
    # Write a function that, given two input numpy arrays, 'data', and 'predictions,'
    # returns the coefficient of determination, R^2, for the model that produced 
    # predictions.
    # 
    # Numpy has a couple of functions -- np.mean() and np.sum() --
    # that you might find useful, but you don't have to use them.

    # YOUR CODE GOES HERE
     
    
    meanD = np.mean(data)
    # option 1
	#   meanD = np.mean(data)
	#   meanP = np.mean(predictions)
	#   print "Data size is " + str(len(data))
	#   print "Pred size is " + str(len(predictions))
	#   print "MeanD=" + str(meanD) + "  MeanP=" + str(meanP)
	#   r_squared = 0
	#   
	#   varSum = 0
	#   for i in range(1,len(data)+1):
	#       #varSum = varSum + ( ( data[i] - meanD) * ( data[i] - meanD ) )
	#       varSum = varSum + ((data[i] - meanD ) * ( (data[i] - meanD ) ))
	#   
	#   errorSum = 0
	#   for j in range(1, len(predictions) ):
	#       #print "j=" + str(j)
	#       errorSum = errorSum + ( (predictions[j] - data[j+1]) * (predictions[j] - data[j+1]) )
	#       
	#   r_squared = 1 - ( errorSum / varSum )
    
    
    # Solution # 2
    varDenom = np.sum( (data-meanD)**2)
    varNum = np.sum( ( data - predictions ) **2)
    
    r_squared = 1- varNum/varDenom
    return r_squared
