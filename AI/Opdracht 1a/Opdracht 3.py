""" Opdracht 3 - Lijstcheck """


def count(lst, n):
    """ Vul in de lijst in "lst". Vul bij "n" een nummer in om te weten hoe vaak dat nummer in de lijst voorkomt"""
    my_dict = {}
    for i in lst:
        if i in my_dict:
            my_dict[i] += 1
        else:
            my_dict[i] = 1
    return my_dict[n]

# lst = [0, 1, 2, 3, 4, 2, 3]
# print(count(lst, 1))


def grootsteverschil(lst):
    max = 0
    for i in range(len(lst) - 1):
        temp = lst[i] - lst[i + 1]
        if temp < 0:
            temp *= -1
        if temp > max:
            max = temp
    return max

# lst = [0, 2, 2, 3, 7]
# print(grootsteverschil(lst))


def lijstcheck(lst):
    number_of_1s = count(lst, 1)
    number_of_0s = count(lst, 0)
    if number_of_1s < number_of_0s:
        return False
    if number_of_0s >= 12:
        return False
    else:
        return True


"""
lst = []
number_of_1s = 13
number_of_0s = 11
for i in range(number_of_1s):
    lst.append(1)
for i in range(number_of_0s):
    lst.append(0)

print(lijstcheck(lst))
"""