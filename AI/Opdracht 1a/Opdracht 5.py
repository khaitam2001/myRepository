""" Opdracht 5 - Sorteren """


def sorteren(lst):
    lst_copy = lst.copy()
    for i in range(len(lst_copy) - 1):
        if lst_copy[i] > lst_copy[i + 1]:
            remember = lst_copy[i]
            lst_copy[i] = lst_copy[i + 1]
            lst_copy[i + 1] = remember
    if lst_copy == lst:
        return lst_copy
    return sorteren(lst_copy)

lst = [1, 3, 9, 3, 2, 1, -1]
print(sorteren(lst))