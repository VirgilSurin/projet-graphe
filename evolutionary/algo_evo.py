from random import *
from copy import deepcopy
from copy import copy


def get_data(datafile):
    l = []
    with open(datafile) as f:
        for line in f:
            l.append(int(line))
    return l
    
#Taille pop
#Nb max de générations
#Proba croisement: [0.5,0.9]
#Proba de mutation: [0.05,0.1]



def generate_pop(size, N, B, E, data):
    pop = []
    for i in range(size):
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
            for item in new_cut:
                ind[indexI].append(item)

            #on retire le nombre d'emplacement qui vient d'être occupé
            left -= (nb_of_cut-1)
        #on rajoute l'individu obtenu à la population
        pop.append(ind)
    return pop




def get_cost(ind, B, E):
    res = []
    l = [] 
    for item in ind:
        for value in item:
            l.append(value)
    l.sort(reverse=True)

    k = 0
    for i in range(B):
        a = []
        for j in range(E):
            a.append(l[k])
            k += 1  
        res.append(a)

    sol = 0
    for i in range(B):
        sol += res[i][0]
    return sol

def select_winner(ind_list, tournament_N, B, E):
    selected = []
    c_ind_list = deepcopy(ind_list)
    proba = 1/tournament_N
    for i in range(tournament_N):
        selected.append(c_ind_list.pop(randint(0,len(c_ind_list)-1)))

    tournament = [get_cost(selected[i], B, E)*proba*(1-proba)**i for i in range(len(selected))]
    winner = selected[tournament.index(max(tournament))]
    return winner

def select_parents(ind_list,tournament_N, B, E):
    available_parents = deepcopy(ind_list)
    new_parents = []
    while len(new_parents) < len(available_parents)/2:
        p1 = select_winner(available_parents, tournament_N, B, E)
        available_parents.remove(p1)
        p2 = select_winner(available_parents, tournament_N,B,E)
        available_parents.remove(p2)
        new_parents.append((p1,p2))
    return new_parents

def cross_parents(p1,p2, cross_prob, B, E):
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
    print("cross")
    return c1, c2

def calculate_e(ind):
    res = 0
    for item in ind:
        res += len(item)
    return res
def normalize_children(c1, c2, B, E):
    a = calculate_e(c1)
    if a != B*E:
        c1 = reequilibrate(c1, a, B, E)
    b = calculate_e(c2)
    if b != B*E:
        c2 = reequilibrate(c2, b, B, E)
    return c1,c2

def reequilibrate(c,l, B, E):
    voyager = 0
    while l > B*E:
        if len(c[voyager]) >= 2:
            c[voyager][-2] += c[voyager][-1]
            c[voyager].pop()
            c[voyager].sort()
            l = calculate_e(c)
        voyager = (voyager + 1)%len(c)
    voyager = 0
    while l < B*E:
        if c[voyager][0]//2 + c[voyager][0] %2 > 1:
            newv1 = c[voyager].pop(0)
            c[voyager].append(newv1//2 + newv1 %2)
            c[voyager].append(newv1//2)
            c[voyager].sort()
            l = calculate_e(c)
        voyager = (voyager + 1)%(len(c))
        

    return c


"""
Recherche Locale
"""

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
    return neighbor
    
    
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


def mutate(c, mutation_prob, data, nb_neighbor, B, E):
    prob = random()
    if prob > mutation_prob:
        return c
    neighborhood = []
    for i in range(nb_neighbor):
        neighborhood.append(generate_random_neighbor(c, data))

    while True:
        find_better_sol = False
        for sol in neighborhood:
            if get_cost(c, B, E) > get_cost(sol, B, E):
                c = sol
                find_better_sol = True
                break
                
        if not find_better_sol:
            break
    print("mutation")
    return c

"""
"""

if __name__ == "__main__":

    #inputs
    datafile = "../samples/data1.dat"
    data = get_data(datafile)
    N = len(data)
    B = 3
    E = 10
    size = 20
    nb_gen = 30
    nb_neighbor = 500

    cross_prob = 0.75
    mutation_prob = 0.085

    pop = generate_pop(size, N, B, E, data)
    for item in pop:
        print(item)
        print("size",calculate_e(item))

    parents = select_parents(pop, size//2, B,E)
    k=1
    for p1,p2 in parents:
        print(k)
        print("p1:", p1)
        print("size p1:", calculate_e(p1), "| cost: ", get_cost(p1, B, E))
        print("p2:", p2)
        print("size p2", calculate_e(p2), "| cost: ", get_cost(p2, B, E))
        c1, c2 = cross_parents(p1, p2, cross_prob, B, E)

        print("c1:", c1)
        print("size c1: ", calculate_e(c1))
        print("c2:", c2)
        print("size c2: ", calculate_e(c2))

        c1, c2 = normalize_children(c1, c2, B, E)
        
        print("child1 normalized : ", c1)
        before1 = get_cost(c1, B, E)
        print("len c1", calculate_e(c1), "cost: ", before1)
        print("child2 normalized: ",c2)
        before2 = get_cost(c2, B, E)
        print("len c2", calculate_e(c2), "cost: ", before2)


        print("TEST MUTATION")
        c1 = mutate(c1, mutation_prob ,data, nb_neighbor, B, E)
        print("Better c1", c1)
        after1 = get_cost(c1, B, E)
        print("len c1", calculate_e(c1), "cost: ", after1)

        c2 = mutate(c2, mutation_prob, data, nb_neighbor, B, E)
        print("Better c2", c2)
        after2 = get_cost(c2, B, E)
        print("len c2", calculate_e(c2), "cost: ", get_cost(c2, B, E))

        print()
        print("P1: ", get_cost(p1, B,E))
        print("P2: ", get_cost(p2, B, E))
        print()
        print("\nC1: Before: ", before1, " After: ", after1)
        print("\nC2: Before: ", before2, " After: ", after2)
        k+=1

