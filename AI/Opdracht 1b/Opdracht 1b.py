""" Opdracht 1b """

from random import randrange
import itertools
import string


def textterminal():
    """ Deze functie zorgt ervoor dat de gebruiker text kan zien dat een spelbord moet voorstellen. Verder worden hier
    ook inputs geplaatst om de gok van de speler op te slaan"""
    pass


def generaterandomcode(number_of_colors=None):
    """ Genereer een lijst met input number_of_colors en de functie "generatecombinationslist".
    Returnt een random nummer in de gemaakte lijst"""
    if number_of_colors == None:
        number_of_colors = generatecombinationslist(6)
    else:
        number_of_colors = generatecombinationslist(number_of_colors)
    return number_of_colors[randrange(0, len(number_of_colors))]


def generatecombinationslist(number_of_colors):
    """ Genereer alle mogelijke combinaties. Returnt een lijst met alle combinaties"""
    # SOURCE = https://stackoverflow.com/questions/464864/how-to-get-all-possible-combinations-of-a-list-s-elements
    list = []
    for i in range(number_of_colors):
        list.append(string.ascii_lowercase[i])
    all_combinations = []
    list_permutations = itertools.permutations(list, len(list))
    for each_permutation in list_permutations:
        all_combinations.append(each_permutation)
    return all_combinations

# print(generatecombinationslist(5))
# print(generaterandomcode(5))


def checkAnswer(guessedanswer, correctanswer):
    """ Deze functie returnt het aantal correct gegokte antwoorden. """
    pass


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