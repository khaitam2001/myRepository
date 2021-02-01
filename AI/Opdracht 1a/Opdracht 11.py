""" Opdracht 11 - Caesarcijfer """


import string


def Caesarcijfer():
    tekst = input("Geef een tekst: ")
    rotatie = int(input("Geef een rotatie: "))

    alphabet_lowercase = string.ascii_lowercase
    alphabet_uppercase = string.ascii_uppercase

    tekst_copy = ""

    for i in tekst:
        if i in alphabet_lowercase:
            location = alphabet_lowercase.find(i)
            tekst_copy += alphabet_lowercase[location + rotatie]
        elif i in alphabet_uppercase:
            location = alphabet_uppercase.find(i)
            tekst_copy += alphabet_uppercase[location + rotatie]
        else:
            tekst_copy += " "
    print("Caesarcode: " + tekst_copy)

Caesarcijfer()