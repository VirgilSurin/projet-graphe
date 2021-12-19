#Utils

from random import *
from copy import deepcopy
from copy import copy

def get_data(datafile):
    """
    Get the data of the problem

    Parameters
    ----------
    datafile: the name of the file containing the data (duh)

    Returns
    -------
    l : a list of data
    N : the number of data
    B : the number of boxes
    E : the storage per box
    """
    l = []
    with open(datafile) as f:
        for line in f:
            l.append(int(line))
    N = l.pop(0)
    E = l.pop(0)
    B = l.pop(0)
    return l, N, B, E
   
def get_data_from_recuit(datafile):
    l = []
    with open(datafile) as f:
        i = 0
        for line in f:
            if line[0] in [str(x) for x in range(1,10)]:
                l.append(line[0:-2])
            i += 1

    for i in range(len(l)):
        l[i] = l[i].split()
        l[i] = l[i][3:]
        l[i] = [int(l[i][k]) for k in range(len(l[i]))]
    print(l)
    return l

def create_pop_from_recuit():
    pop = []
    for i in range(1,11):
        datafile = "outputrecuit/output"+str(i)+".txt"
        ind = get_data_from_recuit(datafile)
        if ind not in pop:
            pop.append(ind)
    print("POP",pop)
    size = len(pop)
    return pop, size

def print_sol(sol, data, N, B, E):
    for i in range(len(sol)):
        s = str(i+1) +" "+ str(data[i]) + " "+ str(len(sol[i]))
        for j in range(len(sol[i])):
            s += " " + str(sol[i][j])
        print(s)

    l = []
    for item in sol:
        for elem in item:
            l.append(elem)
    l.sort(reverse=True)
    cost=0
    for i in range(B):
        max_index = i*E
        s = "B"+str(i+1)+ " " + str(l[max_index])
        print(s)
    print("COST ", get_cost(sol, N, B, E))
    

def generate_pop(size, N, B, E, data):
    """Randomly generates a population of solutions

    Parameters
    ----------
    size: the size of the population
    N : the number of data
    B : the number of boxes
    E : the storage per box
    data: the list of data
    Returns
    -------
    pop : a population of N solutions

    """
    pop = []
    while len(pop) != size:
        ind = []
        for k in range(len(data)):
            ind.append([data[k]])
        left = B*E-N

        #tant qu'il reste de la place
        while left > 0:
            #on choisit les indices de la liste ind, pour séléctionner quelle donnée va être découpée
            indexI = randint(0,N-1)
            indexJ = randint(0,len(ind[indexI])-1)
            chosen_one = ind[indexI][indexJ]

            #on choisit le nombre de fois qu'on va découper
            nb_of_cut = randint(2,left+1)

            #on évite de découper un nombre avec des zéros ou des 1 (à modifier)
            if chosen_one//nb_of_cut <= 1:
                continue
                #todo: treshold

            """
            #nouvelle découpe de la donnée
            new_cut = [chosen_one//nb_of_cut for i in range(nb_of_cut)]
            new_cut[0] += chosen_one%nb_of_cut
            """

            #découpe aléatoire de la donnée
            new_cut = []
            to_split = chosen_one
            for i in range(nb_of_cut-1):
                if to_split > 1:
                    d = randint(1,to_split//2)
                    new_cut.append(d)
                    to_split -= d  
            new_cut.append(to_split)
            new_cut.sort(reverse=True)

            #on retire la donnée et on la remplace par sa nouvelle découpe
            ind[indexI].remove(chosen_one)
            left +=1
            for item in new_cut:
                ind[indexI].append(item)
                left-=1

        #on rajoute l'individu obtenu à la population
        if ind not in pop:
            pop.append(ind)
    return pop

def get_cost(ind,N, B, E):
    """
    Gets the cost of a solution

    Parameters
    ----------
    ind: an indiv/solution
    N : the number of data
    B : the number of boxes
    E : the storage per box
    Returns
    -------
    cost : the cost of the solution
    """
    l = []
    for item in ind:
        for elem in item:
            l.append(elem)
    l.sort(reverse=True)
    cost=0
    for i in range(B):
        max_index = i*E
        cost+=l[max_index]
    return cost


def calculate_e(ind):
    res = 0
    for item in ind:
        res += len(item)
    return res