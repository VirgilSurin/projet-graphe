from mutation import *
from croisement import *
from utils import *




"""
Générations
"""

def evolutionnary(data, N, B, E, size, nb_gen, nb_neighbor, cross_prob, mutation_prob):
    """
    Implementation of the evolutionnary algorithm
        
    Parameters
    ----------
    data: the list of data

    N : the number of data
    B : the number of boxes
    E : the storage per box

    size: the size of the population
    nb_gen : the number of generations
    nb_neighbor : the number of neighbors (for the local search)
    cross_prob : the probability of crossing
    mutation_prob : the probability of mutation
    Returns
    -------
    
    """
    #pop, size = create_pop_from_recuit()

    pop = generate_pop(size, N, B, E, data)
    for item in pop:
        print(get_cost(item, N, B, E))
    for i in range(nb_gen):
        parents = select_parents(pop, size//2,N, B,E)
        pop = []
        for p1, p2 in parents:
            c1, c2 = cross_parents(p1, p2, cross_prob)
            c1, c2 = normalize_children(c1, c2, B, E)
            c1 = mutate(c1, mutation_prob ,data, nb_neighbor,N, B, E)
            c2 = mutate(c2, mutation_prob, data, nb_neighbor,N, B, E)
            next_g = next_gen(p1,p2,c1,c2, N, B, E)
            pop.append(next_g[0])
            pop.append(next_g[1])

    print("END")
    for item in pop:
        print(item)
        print(calculate_e(item), "| cost: ", get_cost(item, N, B, E))
    costs = [get_cost(i, N, B, E) for i in pop]
    min_value = min(costs)
    index = costs.index(min_value)
    print("\n\n\nBest")
    print_sol(pop[index], data, N, B, E)
"""

"""
if __name__ == "__main__":

    #inputs
    datafile = "../samples/data1.dat"
    data, N, B, E = get_data(datafile)
    #Taille pop
    size = 100
    #Nb de générations
    nb_gen = 500
    #Nb de voisins pour recherche locale
    nb_neighbor = 1500

    #Proba croisement: [0.5,0.9]
    cross_prob = 0.85
    #Proba de mutation: [0.05,0.1]
    mutation_prob = 0.01

    evolutionnary(data, N, B, E, size, nb_gen, nb_neighbor, cross_prob, mutation_prob)

    #create_pop_from_recuit()


#Some Tests
"""
    pop = generate_pop(size, N, B, E, data)
    for item in pop:
        print(item)
        print("size",calculate_e(item))

    parents = select_parents(pop, size//3, N, B,E)
    k=1
    new_pop = []
    for p1,p2 in parents:
        print(k)
        print("p1:", p1)
        print("size p1:", calculate_e(p1), "| cost: ", get_cost(p1,N, B, E))
        print("p2:", p2)
        print("size p2", calculate_e(p2), "| cost: ", get_cost(p2,N, B, E))
        c1, c2 = cross_parents(p1, p2, cross_prob)

        print("c1:", c1)
        print("size c1: ", calculate_e(c1))
        print("c2:", c2)
        print("size c2: ", calculate_e(c2))

        c1, c2 = normalize_children(c1, c2, B, E)
        
        print("child1 normalized : ", c1)
        before1 = get_cost(c1, N, B, E)
        print("len c1", calculate_e(c1), "cost: ", before1)
        print("child2 normalized: ",c2)
        before2 = get_cost(c2,N, B, E)
        print("len c2", calculate_e(c2), "cost: ", before2)


        print("TEST MUTATION")
        c1 = mutate(c1, mutation_prob ,data, nb_neighbor,N, B, E)
        print("Better c1", c1)
        after1 = get_cost(c1,N, B, E)
        print("len c1", calculate_e(c1), "cost: ", after1)

        c2 = mutate(c2, mutation_prob, data, nb_neighbor,N, B, E)
        print("Better c2", c2)
        after2 = get_cost(c2,N, B, E)
        print("len c2", calculate_e(c2), "cost: ", get_cost(c2, N, B, E))

        print()
        print("P1: ", get_cost(p1, N, B,E))
        print("P2: ", get_cost(p2, N, B, E))
        print()
        print("C1: Before: ", before1, " After: ", after1)
        print()
        print("C2: Before: ", before2, " After: ", after2)
        next_g = next_gen(p1,p2,c1,c2, B, E)
        print()
        print("Next Gen:")
        print(next_g[0])
        print("len ", calculate_e(next_g[0]), "cost: ", get_cost(next_g[0],N, B, E))
        print(next_g[1])
        print("len ", calculate_e(next_g[1]), "cost: ", get_cost(next_g[1],N, B, E))

        new_pop.append(next_g[0])
        new_pop.append(next_g[1])
        k+=1
    print()
    print()
    print("New Pop:", len(new_pop))
    print(new_pop)
"""