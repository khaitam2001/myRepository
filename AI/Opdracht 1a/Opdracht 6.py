""" Opdracht 6 - Gemiddelde berekenen """


def gemiddelde(lst):
    total = 0
    for number in lst:
        total += number
    return total / len(lst)

# lst = [0, 1, 2, 3, 4]
# print(gemiddelde(lst))


def gemiddeldelijsten(lst):
    gemiddeldelst = []
    for lijst in lst:
        gemiddeldelst.append(gemiddelde(lijst))
    return gemiddeldelst

# lst = [[0, 1, 2], [2, 3, 4], [3, 4, 5]]
# print(gemiddeldelijsten(lst))