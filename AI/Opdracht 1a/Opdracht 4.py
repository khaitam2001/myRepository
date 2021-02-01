""" Opdracht 4 - Palindroom """


def palindroom(woord):
    if len(woord) % 2 == 0:
        middle = int(len(woord) / 2 + 1)
        if woord[0:middle - 1] == woord[:middle - 2:-1]:
            return True
    else:
        middle = int(len(woord) / 2 + 1)
        if woord[0:middle - 1] == woord[:middle - 1:-1]:
            return True
    return False

string = "dood"
print(palindroom(string))