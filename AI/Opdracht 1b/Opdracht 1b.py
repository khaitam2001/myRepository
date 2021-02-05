""" Opdracht 1b """

from random import randrange
import itertools
import string


def textterminal():
    """ Deze functie zorgt ervoor dat de gebruiker text kan zien dat een spelbord moet voorstellen. Je kunt ook het
    totaal aantal kleuren bepalen en hoeveel kleuren je moet gokken. """
    player = input("Voer in de speler 'human' of 'shapiroAI': ")
    if player != 'human' and player != "shapiroAI":
        print("Verkeerde naam, standaard 'human' ingevoerd")
        player = "human"
    try:
        number_of_colors = int(input("Voer het totaal aantal kleuren in waarmee je wilt spelen: "))
    except ValueError:
        print("ValueError, standaard 6 kleuren ingevuld")
        number_of_colors = 6
    try:
        length_of_guess = int(input("Voer het aantal kleuren in dat je moet gokken: "))
        if length_of_guess > number_of_colors:
            print("Te hoog, standaard 4 kleuren ingevuld")
    except ValueError:
        print("ValueError, standaard 4 kleuren ingevuld")
        length_of_guess = 4
    try:
        number_of_tries = int(input("Voer in hoe vaak je mag gokken: "))
    except ValueError:
        print("ValueError, standaard 8 pogingen ingevuld")
        number_of_tries = 8
    secret_code = generaterandomcode(number_of_colors, length_of_guess)
    print("(dit hoort de speler niet te zien) De geheime code is: " + str(secret_code))

    answerguessed = False

    """ Dit deel is gemaakt voor de speler. Dit stuk zorgt ervoor dat de speler het spel kan spelen"""
    while answerguessed == False and number_of_tries > 0 and player == "human":
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
            number_of_tries -= 1
            print("Je hebt nog " + str(number_of_tries) + " pogingen.")
            print(feedback)

    """ Dit deel is gemaakt voor de shapiroAI. Het zorgt ervoor dat de functies die nodig zijn worden aangeroepen """
    possiblelist = generatecombinationslist(number_of_colors, length_of_guess)
    while answerguessed == False and number_of_tries > 0 and player == "shapiroAI":
        guess = shapiroAI(possiblelist)
        print("De computer gokt: " + str(guess))
        feedback = checkAnswer(guess, secret_code)
        if guess == secret_code:
            answerguessed = True
            print("Correct! Computer heeft gewonnen")
        else:
            possiblelist = generatepossiblecombinationslist(possiblelist, guess, feedback)
            number_of_tries -= 1
        if number_of_tries == 0:
            print("Computer heeft verloren!")


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


def generatepossiblecombinationslist(lst=None, guess=None, feedback=None):
    """ Bekijkt of dezelfde feedback uit een mogelijke antwoord en gok komt. Returnt een lijst met mogelijke goede
    antwoorden """
    list_copy = []
    for possibleanswer in lst:
        if checkAnswer(guess, possibleanswer) == feedback:
            list_copy.append(possibleanswer)
    return list_copy


def checkAnswer(guessedanswer, correctanswer):
    """ Returnt een boolean met guessedanswer == correctanswer. Als het niet klopt wordt er feedback gegeven"""
    if guessedanswer == list(correctanswer):
        return True
    else:
        my_dict = {"zwart":0,"wit":0}
        guessedanswer_copy = list(guessedanswer).copy()
        for i in range(len(guessedanswer)):
            if guessedanswer[i] == correctanswer[i]:
                my_dict["zwart"] += 1
                guessedanswer_copy.remove(guessedanswer[i])
        for i in range(len(guessedanswer_copy)):
            for index in range(len(correctanswer)):
                if guessedanswer_copy[i] == correctanswer[index]:
                    my_dict["wit"] += 1
        return my_dict


def shapiroAI(possiblelist):
    """ Returnt een random mogelijkheid van de lijst die wordt gegeven"""
    return possiblelist[randrange(0, len(possiblelist))]


def onestepaheadAI():
    """ Deze functie zorgt ervoor dat er een tegenstander is waar de gebruiker tegen kan spelen. De manier waarop
    de AI keuzes maakt, is gebaseerd op een stap vooruit kijken. """
    pass


def eenkleurAI():
    """ Deze functie zorgt ervoor dat er een tegenstander is waar de gebruiker tegen kan spelen. De manier waarop
    de AI keuzes maakt, is gebaseerd op een kleur kiezen. Daarna gebaseerd op de feedback worden andere keuzes gemaakt
    """
    pass


textterminal()
# print(generatecombinationslist(5, 6))
# print(generaterandomcode(6, 7))