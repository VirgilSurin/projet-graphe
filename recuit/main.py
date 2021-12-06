import random


def solve(s,T,Tf,N, input_numbers):
    """
    s -> solution initiale
    T -> temperature initiale
    Tf -> temperature finale
    decreasing -> pourcentage de decroissance
    N -> nombre d'etape a la meme temperature
    """
    s = getInitSolution()
    e = cost(s)
    best_s = s
    best_e = e
    while T > Tf :
        for k in range(N):
            sn = generate_random_neighbor(input_numbers, s)
            en = cost(sn)
            if (en < e) or (random.random() < prob(e-en, T)):
                s = sn
                e = en
                if best_e > e:
                    best_s = s
                    best_e = e
        T *= decreasing
    return best_s


def prob(de, T):
    return e^(-de/T)


def generate_random_neighbor(input_numbers, sol):
    """
    given a sol, will swap and create a neighbor.
    """
    neighbor = []
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
    sol[i] = new_i
    sol[j] = new_j
    
    
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
init_sol = [[2430, 2430, 2240, 560], \
            [2430, 2430, 2430], \
            [2430, 2430, 2180], \
            [2430, 2240, 2220], \
            [2430, 2240, 610, 580], \
            [2430, 2240, 610], \
            [2430, 2210], \
            [2240, 610, 610, 370], \
            [2240, 610, 610], \
            [580]]


