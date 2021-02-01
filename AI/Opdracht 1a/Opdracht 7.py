""" Opdracht 7 - Random """


import random


def randomguess():
    numberIsGuessed = False
    randomNumber = random.randint(0, 100000)
    # print(randomNumber)
    while numberIsGuessed == False:
        gok = input("Gok het getal: ")
        if int(gok) == randomNumber:
            print("Goedgeraden")
            numberIsGuessed = True
        else:
            print("\nVerkeerd getal \n")

# randomguess()