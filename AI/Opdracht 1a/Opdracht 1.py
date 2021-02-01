"""Opdracht 1 - Pyramide """


def pyramideforloop(n):
    for i in range(n):
        symbol = "*"
        symbol *= i
        print(symbol)
    for i in range(n, 0, -1):
        symbol = "*"
        symbol *= i
        print(symbol)

# pyramideforloop(6)

def pyramidewhileloop(n):
    i = 0
    while i < n:
        symbol = "*"
        symbol *= i
        print(symbol)
        i += 1
    while i > 0:
        symbol = "*"
        symbol *= i
        print(symbol)
        i -= 1

# pyramidewhileloop(6)

def pyramideanderekant(n):
    for i in range(n, 0, -1):
        symbol = "*"
        empty = " "
        symbol *= n - i
        empty *= i
        print(empty+symbol)
    for i in range(n):
        symbol = "*"
        empty = " "
        symbol *= n - i
        empty *= i
        print(empty+symbol)


# pyramideanderekant(6)