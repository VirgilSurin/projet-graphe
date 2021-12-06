import random
from copy import deepcopy

def crossing2Points(parent_1, parent_2):
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
    2 new arrays of arrays of int, the 'children' solutions.
    """
    if !(len(sol_1) == len(sol_2)):
        raise ValueError("Illegal arguments: sizes do not match!")
    else:
        child_1 = []
        child_2 = []
        crossingPoints = []
        crossingPoints.append(getCrossingPoint)
        crossingPoints.append(getCrossingPoint)
        crossingPoints.sort()
        
        for array1 in parent_1:
            for array2 in parent_2:
                child_1.append(
                    array1[: crossingPoints[0]]
                    + (array2[crossingPoints[0] + 1 : crossingPoints[1]])
                    + (array1[crossingPoints[1] + 1 :]))
                child_2.append(
                    array2[: crossingPoints[0]]
                    + (array1[crossingPoints[0] + 1 : crossingPoints[1]])
                    + (array2[crossingPoints[1] + 1 :]))

        return child_1, child_2
        

def getCrossingPoint():
    point = random.randint()
    return point
