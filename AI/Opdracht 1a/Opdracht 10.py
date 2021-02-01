""" Opdracht 10 - Fibonaci """


def fibonaci(n, previousnumber=0, currentnumber=1):
    if n == 1:
        return currentnumber
    return fibonaci(n - 1, currentnumber, previousnumber + currentnumber)

print(fibonaci(9))