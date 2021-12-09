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
    s = get_init_solution(N, B, E, input_numbers)
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
    return exp(de/T)


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
    total_split = len(sol[i]) + len(sol[j])
    i_split = random.randint(1, total_split-1)
    j_split = total_split - i_split
    # we know the number of splits for each number
    # biggest = max([max(sublist) for sublist in sol])
    # new_i = smarter_split(input_numbers[i], biggest, j_split)[0]
    # new_j = smarter_split(input_numbers[j], biggest, i_split)[0]
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

def smarter_split(x, biggest, n=None):
    """
    given the biggest split, will split the number x without going above biggest.
    If n is specified, will split it in maximum n number.
    Return an array with all the splits and the number of splits made and the biggest number
    """
    # TODO does not work
    if x <= biggest:
        return [x], 1, biggest
    else:
        if n != None:
            res = []
            while x >= biggest and n > 1:
                x -= biggest
                res.append(biggest)
                n -= 1
            if n > 1:
                if x > 0:
                    res.append(x)
                    n -= 1
                while n > 0:
                    res.append(0)
                    n -= 1
                if x > biggest and n > 0:
                    return res, len(res), x
                else:
                    return res, len(res), biggest
            else:
                if x > 0 and n > 0:
                    res.append(x)
                    n -= 1
                if x > biggest and n > 0:
                    return res, len(res), x
                else:
                    return res, len(res), biggest
        else:
            res = []
            while x >= biggest:
                x -= biggest
                res.append(biggest)
            if x > 0:
                res.append(x)
            if x > biggest:
                return res, len(res), x
            else:
                return res, len(res), biggest
            

def get_init_solution(N, B, E, input_numbers):
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


def resolve(filename):
    filepath = "../samples/" + filename
    f = open(filepath, "r")
    N = int(f.readline())
    E = int(f.readline())
    B = int(f.readline())
    input_numbers = [int(line) for line in f.readlines()]
    return cost(solve(1000, 5, 0.7, 1000, input_numbers, N, B, E), N, B, E)



filenames = ["data1.dat", "data2.dat", "data3.dat", "data4.dat", "data5.dat", "data6.dat", "data7.dat", "data8.dat", "data9.dat", "data10.dat"]
score_prof = [5243, 8190, 3897, 9978, 4966, 15030, 7194, 239778, 229428, 226788]
[print("Problem " + filenames[i] + " : " + str(resolve(filenames[i])) + " vs " + str(score_prof[i]) + " | diff: " + str(score_prof[i] - resolve(filenames[i])) + " => " + str(((score_prof[i] - resolve(filenames[i]))/score_prof[i])*100)) for i in range(len(filenames))]

