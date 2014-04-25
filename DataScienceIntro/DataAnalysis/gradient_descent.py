#!/usr/bin/python
import numpy
import pandas

def normalize_features(array):
   """
   Normalize the features in our data set.
   """
   array_normalized = (array-array.mean())/array.std()
   mu = array.mean()
   sigma = array.std()

   return array_normalized, mu, sigma



def compute_cost(features, values, theta):
    """
    Compute the cost function given a set of features / values, and values for our thetas.
    """
    m = len(values)
    sum_of_square_errors = numpy.square(numpy.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2*m)

    return cost

def gradient_descent(features, values, theta, alpha, num_iterations):
    """
    Perform gradient descent given a data set with an arbitrary number of features.
    """

    # Write some code here that updates the values of theta a number of times equal to
    # num_iterations.  Everytime you have computed the cost for a given set of thetas,
    # you should append it to cost_history.  The function should return both the final
    # values of theta and the cost history.

    # YOUR CODE GOES HERE
    m = len(values)
    cost_history = []
    for i in range(num_iterations):
        predicted_values = numpy.dot(features,theta)
        theta = theta - alpha / m * numpy.dot(predicted_values - values, features)
        cost_history.append(compute_cost(features, values, theta))
        
    return theta, pandas.Series(cost_history)


data = pandas.read_csv("../files/baseball_data.csv")
features = data[['height', 'weight']]
values = data[['HR']]
m = len(values)

features, mu, sigma = normalize_features(features)
#theta = numpy.matrix('0 0 0 ')
gradient_descent(features, values, theta,.01, 1000)

