import random
from copy import deepcopy
from math import exp

def solve(T, Tf, decreasing, step, input_numbers, N, B, E):
    """
    T -> temperature initiale
    Tf -> temperature finale
    decreasing -> pourcentage de decroissance
    step -> nombre d'etape a la meme temperature
    """
    s = get_init_solution()
    e = cost(s, N, B, E)
    best_s = s
    best_e = e
    while T > Tf :
        for k in range(step):
            sn = generate_random_neighbor(input_numbers, s)
            en = cost(sn, N, B, E)
            if (en < e) or (random.random() < prob(e-en, T)):
                s = sn
                e = en
                if best_e > e:
                    best_s = s
                    best_e = e
        T *= decreasing
    return best_s


def prob(de, T):
    return exp(-de/T)


def cost(sol,N,B,E):
    """Get the cost of a solution

    Parameters
    ----------
    sol : array of array of int (lol)
        The solution 
    N : int
        Length of the input data
    B : int
        Number of boxes in which the data have to be split in
    E : int 
        Size of the boxes

    Returns
    -------
    int
        The cost of the input solution
    """
    l = []
    for i in range(N):
        for j in range(len(sol[i])):
            l.append(sol[i][j])
    l.sort(reverse=True)
    cost=0
    for i in range(B):
        max_index = i*E
        cost+=l[max_index]
    return cost


def generate_random_neighbor(input_numbers, sol):
    """
    given a sol, will swap and create a neighbor.
    """
    neighbor = deepcopy(sol)
    # we generate a neighbor by swaping the number of split of two number
    
    # we choose two number to swap
    i, j = 0, 0
    while i == j:
        i = random.randint(0, len(input_numbers)-1)
        j = random.randint(0, len(input_numbers)-1)
    
    # print(str(i) + " | " + str(j) + " / " + str(len(sol)) + " = " + str(len(input_numbers)))
    i_split = len(sol[i])
    j_split = len(sol[j])
    # we know the number of splits for each number
    new_i = split(input_numbers[i], j_split)
    new_j = split(input_numbers[j], i_split)
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

# samples data1.dat
input_numbers = [7660, 7290, 7040, 6890, 5860, 5090, 4640, 3830, 3460, 580]

N = 10
B = 3
E = 10



def get_init_solution():
    sol=[]
    for i in range(N):
        sol.append([input_numbers[i]])
    for i in range(B * E - N) :
        index=i%N
        end = len(sol[index])-1
        num = sol[index][end]           
        (a,b) = split(num,2)
        sol[index][end] = a
        sol[index].append(b)
    return sol

print(cost(get_init_solution() , N , B , E))

res = solve(100000, 5, 0.01, 10000, input_numbers, N, B, E)
print(res)
print(cost(res, N, B, E))
