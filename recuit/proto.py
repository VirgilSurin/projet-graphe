# input format is
"""
N
E
B
N lines with a number
"""

def resolve2(filename):
    filepath = "./samples/" + filename
    f = open(filepath, "r")
    N = int(f.readline())
    E = int(f.readline())
    B = int(f.readline())
    numbers = [int(line) for line in f.readlines()]
    places_left = E*B
    res = []
    splits = []
    [splits.append([]) for i in range(len(numbers))]
    while places_left > 0:
        maxi = max(numbers)
        if maxi >= 0:
            index = numbers.index(maxi)
            numbers[index] = -1  # we already split that one

            a = maxi//2
            b = (maxi//2) + maxi%2
            res.append(a)
            res.append(b)
            # we know which number is split in what
            # print("INDEX : " + str(index))
            splits[index].append(a)
            splits[index].append(b)
        # print("NUMB : " + str(numbers))
        # print("SPLT : " + str(splits))
        places_left -= 1
        
    res_str = []
    for i in range(len(numbers)):
        res_str.append(str(sum(splits[i])) + " " + str(len(splits[i])) + " " + " ".join([str(splits[i][j]) for j in range(len(splits[i]))]))
    # we need to clear the -1 in numbers
    filtered_numbers = list(filter(lambda numb : numb>=0, numbers))
    res += filtered_numbers
    res.sort()
    
    # now we need to seperate in B box
    sep_size = len(res)//B
    index = 0
    final = []
    for i in range(B):
        final.append(res[index])
        index += sep_size
    for i in range(len(final)):
        res_str.append("B" + str(i+1) + " " + str(final[i]))
    res_str.append("COST " + str(sum(final)))
    return res_str, E*B, N*2

def resolve(filename):
    filepath = "./samples/" + filename
    f = open(filepath, "r")
    N = int(f.readline())
    E = int(f.readline())
    B = int(f.readline())
    numbers = [int(line) for line in f.readlines()]
    places_left = E*B
    res = []
    while places_left > 0:
        if len(numbers) != 0:
            maxi = max(numbers)
            numbers.remove(maxi)
            a = maxi//2
            b = (maxi//2) + maxi%2
            res.append(a)
            res.append(b)
        places_left -= 1
    res += numbers
    res.sort()

    # now we need to seperate in B box
    sep_size = len(res)//B
    index = 0
    final = []
    for i in range(B):
        final.append(res[index])
        index += sep_size
    score = sum(final)
    return score

filenames = ["data1.dat", "data2.dat", "data3.dat", "data4.dat", "data5.dat", "data6.dat", "data7.dat", "data8.dat", "data9.dat", "data10.dat"]
score_prof = [5243, 8190, 3897, 9978, 4966, 15030, 7194, 239778, 229428, 226788]
# [print("Problem " + filenames[i] + " : " + str(resolve(filenames[i])) + " vs " + str(score_prof[i]) + " | diff: " + str(score_prof[i] - resolve(filenames[i]))) for i in range(len(filenames))]
for i in range(len(filenames)):
    print("-------------------------" + filenames[i] + "-------------------------")
    yeet = resolve2(filenames[i])
    [print(line) for line in yeet[0]]
    print("places : " + str(yeet[1]) + " | Taken : " + str(yeet[2]))

