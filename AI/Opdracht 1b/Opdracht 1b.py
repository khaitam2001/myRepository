""" Opdracht 1b """

from random import randrange
import itertools
import string


def textterminal():
    """ Deze functie zorgt ervoor dat de gebruiker text kan zien dat een spelbord moet voorstellen. Je kunt ook het
    totaal aantal kleuren bepalen en hoeveel kleuren je moet gokken. """
    try:
        number_of_colors = int(input("Voer het totaal aantal kleuren in waarmee je wilt spelen: "))
    except ValueError:
        print("ValueError, standaard 6 kleuren ingevuld")
        number_of_colors = 6
    try:
        length_of_guess = int(input("Voer het aantal kleuren in dat je moet gokken: "))
    except ValueError:
        print("ValueError, standaard 4 kleuren ingevuld")
        length_of_guess = 4
    secret_code = generaterandomcode(number_of_colors, length_of_guess)
    print("(dit hoort de speler niet te zien) De geheime code is: " + str(secret_code))

    answerguessed = False
    while answerguessed == False:
        try:
            all_guesses = []
            for i in range(length_of_guess):
                guess = input("Voer gok nummer " + str(i + 1) + " in: ")
                all_guesses.append(guess)
        except ValueError:
            print("ValueError")
        feedback = checkAnswer(all_guesses, secret_code)
        if feedback == True:
            answerguessed = True
            print("Correct! Je hebt gewonnen")
        else:
            print(feedback)

def generaterandomcode(number_of_colors=6, length_of_guess=4):
    """ Genereer een lijst met input number_of_colors en de functie "generatecombinationslist".
    Returnt een random nummer in de gemaakte lijst"""
    number_of_colors = generatecombinationslist(number_of_colors, length_of_guess)
    return number_of_colors[randrange(0, len(number_of_colors))]


def generatecombinationslist(number_of_colors=6, length_of_guess=4):
    """ Genereer alle mogelijke combinaties. Returnt een lijst met alle combinaties"""
    # SOURCE = https://stackoverflow.com/questions/464864/how-to-get-all-possible-combinations-of-a-list-s-elements
    list = []
    for i in range(number_of_colors):
        list.append(string.ascii_lowercase[i])
    all_combinations = []
    list_permutations = itertools.permutations(list, length_of_guess)
    for each_permutation in list_permutations:
        all_combinations.append(each_permutation)
    return all_combinations


def checkAnswer(guessedanswer, correctanswer):
    """ Returnt een boolean met guessedanswer == correctanswer. Als het niet klopt wordt er feedback gegeven"""
    if guessedanswer == list(correctanswer):
        return True
    else:
        my_dict = {"zwart":0,"wit":0}
        for i in range(len(guessedanswer)):
            if guessedanswer[i] == correctanswer[i]:
                my_dict["zwart"] += 1
            else:
                for index in range(len(guessedanswer)):
                    if guessedanswer[i] == correctanswer[index]:
                      my_dict["wit"] += 1
        return my_dict


textterminal()
# print(generatecombinationslist(5))
# print(generaterandomcode(5))


def shapiroAI():
    """ Deze functie zorgt ervoor dat er een tegenstander is waar de gebruiker tegen kan spelen. De manier waarop
    de AI keuzes maakt, is gebaseerd op de strategie van Shapiro"""
    pass


def onestepaheadAI():
    """ Deze functie zorgt ervoor dat er een tegenstander is waar de gebruiker tegen kan spelen. De manier waarop
    de AI keuzes maakt, is gebaseerd op een stap vooruit kijken. """
    pass


def eenkleurAI():
    """ Deze functie zorgt ervoor dat er een tegenstander is waar de gebruiker tegen kan spelen. De manier waarop
    de AI keuzes maakt, is gebaseerd op een kleur kiezen. Daarna gebaseerd op de feedback worden andere keuzes gemaakt
    """
    pass