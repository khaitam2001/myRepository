""" Opdracht 9 - Cyclisch verschuiven """


def cyclischverschuiven(character, n):
    index = 0
    if n > 0:
        while index < n:
            character += character[0]
            character = character[1:]
            index += 1
    else:
        n *= -1
        while index < n:
            character += character[-1]
            character = character[0:-1]
            index += 1
    return character

print(cyclischverschuiven('100011', 1))