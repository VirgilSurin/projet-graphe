#Croisement
from utils import get_cost, calculate_e
from random import *
from copy import deepcopy
from copy import copy

def select_winner(ind_list, tournament_N, N, B, E):
    """Selects an individual among a list of selected participants (size = tournament_N)
        If len(ind_list) < tournament_N, returns randomly a winner
        
    Parameters
    ----------
    ind_list : the list of indiv/solutions
    tournament_N : the size of the tournament
    N : the number of data
    B : the number of boxes
    E : the storage per box
    Returns
    -------
    winner : the winner of the tournament
    """
    selected = []
    c_ind_list = deepcopy(ind_list)
    proba = 1/tournament_N
    if len(c_ind_list) < tournament_N:
        shuffle(c_ind_list)
        return c_ind_list[0]
    for i in range(tournament_N):
        selected.append(c_ind_list.pop(randint(0,len(c_ind_list)-1)))

    tournament = [get_cost(selected[i], N, B, E)*proba*(1-proba)**i for i in range(len(selected))]
    winner = selected[tournament.index(max(tournament))]
    return winner

def select_parents(ind_list,tournament_N, N, B, E):
    """Selects two indiv as new parents with the roulette selection
        
    Parameters
    ----------
    ind_list : the list of indiv/solutions
    tournament_N : the size of the tournament
    N : the number of data
    B : the number of boxes
    E : the storage per box
    Returns
    -------
    new_parents : a list of tuple representing the formed couples
    """
    available_parents = deepcopy(ind_list)
    available_len = len(available_parents)
    new_parents = []
    while len(new_parents) < available_len/2:
        p1 = select_winner(available_parents, tournament_N, N, B, E)
        available_parents.remove(p1)
        p2 = select_winner(available_parents, tournament_N, N, B,E)
        available_parents.remove(p2)
        new_parents.append((p1,p2))
    return new_parents

def cross_parents(p1,p2, cross_prob):
    """Crosses two parents to make 2 new children/solutions
        
    Parameters
    ----------
    p1 : parent 1
    p2 : parent 2
    cross_prob : the probability of crossing (between [0.5,0.9])
    B : the number of boxes
    E : the storage per box
    Returns
    -------
    c1 : child 1
    c2 : child 2
    """
    prob = random()
    if prob > cross_prob:
        return p1,p2
    if not(len(p1) == len(p2)):
        raise ValueError("Illegal arguments: sizes do not match!")

    c1 = []
    c2 = []

    crossPoint = randint(0, len(p1))

    for i in range(0, len(p1)):
        if(i < crossPoint):
            c1.append(copy(p1[i]))
            c2.append(copy(p2[i]))
        else:
            c1.append(copy(p2[i]))
            c2.append(copy(p1[i]))

    return c1, c2


def normalize_children(c1, c2, B, E):
    """Will reequilibrate the children if they aren't admissible solutions
        
    Parameters
    ----------
    c1 : potentially inadmissible child 1
    c2 : potentially inadmissible child 2
    B : the number of boxes
    E : the storage per box
    Returns
    -------
    c1 : admissible child 1
    c2 : admissible child 2
    """
    a = calculate_e(c1)
    if a != B*E:
        c1 = reequilibrate(c1, a, B, E)
    b = calculate_e(c2)
    if b != B*E:
        c2 = reequilibrate(c2, b, B, E)
    return c1,c2

def reequilibrate(c,l, B, E):
    """Will reequilibrate a child if they aren't admissible solution
        
    Parameters
    ----------
    c : inadmissible child 1
    l : length of space left (if l < B*E) or overflow (if l > B*E) 
    B : the number of boxes
    E : the storage per box
    Returns
    -------
    c : admissible child
    """
    voyager = len(c)-1
    while l > B*E:
        if len(c[voyager]) >= 2:
            c[voyager][-2] += c[voyager][-1]
            c[voyager].pop()
            c[voyager].sort(reverse=True)
            l = calculate_e(c)
        voyager = (voyager - 1)%len(c)
    voyager = 0
    while l < B*E:
        if c[voyager][0]//2 + c[voyager][0] %2 > 2:
            newv1 = c[voyager].pop(0)
            c[voyager].append(newv1//2 + newv1 %2)
            c[voyager].append(newv1//2)
            c[voyager].sort(reverse=True)
            l = calculate_e(c)
            voyager = (voyager + 1)%len(c)

    return c

