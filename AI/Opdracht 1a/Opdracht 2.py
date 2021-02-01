""" Opdracht 2 - Tekstcheck"""


def tekstcheck():
    string1 = input("Geef een string: ")
    string2 = input("Geef een string: ")
    verschil = 0
    for i in range(len(string1)):
        if string1[i] == string2[i]:
            verschil += 1
        else:
            print("Het eerste verschil zit op index: " + str(verschil - 1))

# tekstcheck()