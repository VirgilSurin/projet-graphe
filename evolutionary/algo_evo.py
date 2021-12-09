from random import *
from copy import deepcopy
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

            #nouvelle découpe de la donnée
            new_cut = [chosen_one//nb_of_cut for i in range(nb_of_cut)]
            new_cut[0] += chosen_one%nb_of_cut

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

"""
"""



if __name__ == "__main__":
    datafile = "../samples/data1.dat"
    data = get_data(datafile)
    N = len(data)
    B = 3
    E = 10
    size = 20
    pop = generate_pop(size, N, B, E, data)
    parents = select_parents(pop, size//2, B,E)
    k=1
    for p1,p2 in parents:
        print(k)
        print("p1:", p1)
        print("p2:", p2)
        print("")
        k+=1
