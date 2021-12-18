from random import *
from copy import copy
from algo_evo import split

def crossingEureka(parent_1, parent_2, cross_proba, initial_list):
    """
    Crosses 2 parent solutions to get 2 children solutions, with a probability, given a rate.
    
    Parameters
    ----------
    parent_1 : array of arrays of int
               a solution to the problem that has been selected for crossing
    parent_2 : array of arrays of int
               a second solution selected for crossing

    Returns
    -------
    2 new arrays of arrays of int, the 'children' solutions.
    """
    proba = random() #generates probabilité of crossing

    if proba > cross_proba: #probability is not checked, no crossing is done
        return parent_1, parent_2
    if not(len(parent_1) == len(parent_2)): #see exception message
        raise ValueError("Illegal arguments: sizes do not match!")
    
    child_1 = conceiveChild(parent_1, parent_2, initial_list) #children are currently list of numbers of splits to make to the initial value
    child_2 = conceiveChild(parent_2, parent_1, initial_list)
        
    child_1 = computeChild(child_1, initial_list) #children are now proper solutions
    child_2 = computeChild(child_2, initial_list)
    
    return child_1, child_2


def conceiveChild(parent_1, parent_2, initial_list):
    """
    Crosses 2 parent solutions to get 2 children solutions.
    
    Parameters
    ----------
    parent_1 : array of arrays of int
               a solution to the problem that has been selected for crossing
    parent_2 : array of arrays of int
               a second solution selected for crossing

    Returns
    -------
    a new array of int, the numbers of split to compute 'children' solutions.
    """
    print("DATA: ", initial_list)
    child = [len(splitted_value) for splitted_value in parent_2] #initialise child 1 as parent 2 lengths for crossing with parent 1
    #works as a window, sliding
    maximum = max(parent_2)
    minimum = min(parent_2)
    print("MAX MIN: ", maximum, minimum)
    i = 0 #init window
    while (len(child) - i) >= 2: #while untouched part size remains greater than the size of the window (that being 2)
        if isGreaterThreshold(initial_list[i],maximum, minimum):
            if len(parent_1[i]) > child[i]:
                compensation_buffer = len(parent_1[i]) - child[i]
                child[i]   += compensation_buffer
                child[i+1] -= compensation_buffer #compensate so as to remain and eligible solution
        elif not(isGreaterThreshold(child[i], maximum, minimum)):
            if len(parent_1[i]) < child[i]:
                compensation_buffer = child[i] - len(parent_1[i])
                child[i]   -= compensation_buffer
                child[i+1] += compensation_buffer #see up
        i+=1 # TODO: may need to be +2 as to negate exponential compensation
    return child
    

def isGreaterThreshold(value, maximum, minimum):
    """
    Acts as a threshold, determines if number is closer to the maximum (or the minimum if not) of the start numbers.

    Parameters
    ----------
    value: int
           the value to compare
    maximum: int
             the maximum value to compare to
    minimum: int
             the minimum value to compare to

    Returns
    -------
    a boolean: True if the value is strictly greater than the mean of min and max
          else False
    """
    mean = (maximum[0] + minimum[0])/2

    return (value > mean)


def computeChild(child, initial_list):
    """
    Crosses 2 parent solutions to get 2 children solutions.
    
    Parameters
    ----------
    child :       array of int
                  a list of number in which to split the initial values to obtain a child
    initial_list: array of int
                  the initial list of solutions

    Returns
    -------
    a new array of arrays of int, the 'child' solution.
    """
    print("CHILD: ", child)
    for i in len(child):
        child[i] = split(initial_list[i], child[i])

    return child
    
