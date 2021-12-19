#Mutation
from random import *
from copy import deepcopy
from copy import copy
from utils import get_cost

#for local search
def generate_random_neighbor(sol, data):
    """
    given a sol, will swap and create a neighbor.
    """
    neighbor = deepcopy(sol)
    # we generate a neighbor by swaping the number of split of two number
    
    # we choose two number to swap
    i, j = 0, 0
    while i == j:
        i = randint(0, len(data)-1)
        j = randint(0, len(data)-1)
    
    # print(str(i) + " | " + str(j) + " / " + str(len(sol)) + " = " + str(len(input_numbers)))
    total_split = len(sol[i]) + len(sol[j])
    i_split = randint(1, total_split-1)
    j_split = total_split - i_split
    new_i = split(data[i], i_split)
    new_j = split(data[j], j_split)

    
    # now we replace
    neighbor[i] = new_i
    neighbor[j] = new_j
    for i in range(len(neighbor)):
        neighbor[i].sort(reverse=True)
    return neighbor
    
#for local search
def split(x, n):
    """
    given a number x, will split it in n equal part.
    If not possible, it will be the "most equal part possible".
    """
    res = []
    if x%n == 0:
        # just need to put the result of x//n n times in res.
        part = x//n
        for i in range(n):
            res.append(part)
    else:
        # stolen from : https://www.geeksforgeeks.org/split-the-number-into-n-parts-such-that-difference-between-the-smallest-and-the-largest-part-is-minimum/
        # upto n-(x % n) the values
        # will be x/n
        # after that the values
        # will be (x/n) + 1
        zp = n - (x % n)
        pp = x//n
        for i in range(n):
            if(i >= zp):
                res.append(pp+1)
            else:
                res.append(pp)
    return res





def mutate(c, mutation_prob, data, nb_neighbor,N, B, E):
    prob = random()
    if prob > mutation_prob:
        return c
    neighborhood = []
    for i in range(nb_neighbor):
        neighborhood.append(generate_random_neighbor(c, data))

    while True:
        find_better_sol = False
        for sol in neighborhood:
            if get_cost(c, N,B, E) > get_cost(sol,N, B, E):
                c = sol
                find_better_sol = True
                break
                
        if not find_better_sol:
            break
    return c

def next_gen(p1, p2, c1, c2, N, B, E):
    """
    Chooses the two best individuals among the parents and children
        
    Parameters
    ----------
    p1 : parent 1
    p2 : parent 2
    c1 : child 1
    c2 : child 2
    N : the number of data
    B : the number of boxes
    E : the storage per box
    Returns
    -------
    next_g : the two best individuals for the next gen
    """
    next_g = []
    cand = [p1, p2, c1, c2]
    costs = [get_cost(p1,N,B,E), get_cost(p2,N,B,E), get_cost(c1,N,B,E), get_cost(c2,N,B,E)]
    while len(next_g) < 2 and len(cand) > 0: 
        min1 = min(costs)
        index = costs.index(min1)
        if cand[index] not in next_g:
            costs.pop(index)
            next_g.append(cand.pop(index))
        else:
            costs.pop(index)
            cand.pop(index)
    if len(next_g) < 2:
        cand = [p1, p2, c1, c2]
        shuffle(cand)
        next_g.append(cand[0])
    return next_g