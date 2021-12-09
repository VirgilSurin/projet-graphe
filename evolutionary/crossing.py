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
    if not(len(parent_1) == len(parent_2)):
        raise ValueError("Illegal arguments: sizes do not match!")
    else:
        child_1 = []
        child_2 = []
        crossingPoints = []
        crossingPoints.append(random.randint(1, len(parent_1)))
        crossingPoints.append(crossingPoints[0] +
                              random.randint(1, len(parent_1)))
        
        for array1 in parent_1:
            for array2 in parent_2:
                child_1.append(deepcopy(
                    array1[: crossingPoints[0]]
                    + (array2[crossingPoints[0] + 1 : crossingPoints[1]])
                    + (array1[crossingPoints[1] + 1 :])))
                child_2.append(deepcopy(
                    array2[: crossingPoints[0]]
                    + (array1[crossingPoints[0] + 1 : crossingPoints[1]])
                    + (array2[crossingPoints[1] + 1 :])))

        return child_1, child_2
