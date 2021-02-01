""" Opdracht 8 - Compressie """

def compress(textbestand):
    f = open(textbestand, "r")
    lst = f.readlines()
    lst_copy = lst.copy()
    index = 0
    for i in lst:
        if "\n" in i:
            lst_copy[index] = i[0:i.find("\n")]

        if " " in i and i.find(" ") == 0:

            emptycount = 0
            for empty in i:
                if empty == " ":
                    emptycount += 1
                else:
                    lst_copy[index] = lst_copy[index][emptycount:]
                    break
        index += 1
    return lst_copy

# compressed = compress("Opdracht8text.txt")

def writefile(filenaam):
    file = open(filenaam, "w+")
    for i in compressed :
        file.write(i + "\n")
    file.close()

# writefile("Opdracht8nieuwetext.txt")
