from myRepository.IPASS.Schaakstukken.Chesspiece import ChessPiece
import string


class Bishop(ChessPiece):
    # De bishop kan diagonaal aanvallen.

    def getLegalMoves(self):
        # Return een lijst met squares die kunnen worden aangevallen door een bishop
        possibleAttackSquares = []

        # Loop door alle squares die North East van het schaakstuk zit.
        for square in self.getAttackSquaresDiagNE():
            # Als er niks op die square staat, dan kan de bishop er naartoe.
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            # Als er wel iets op die square staak, dan moeten we kijken of het van het andere team is of niet.
            else:
                # Check hier of het van hetzelfde team is of niet.
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    # Als het niet hetzelfde team is, dan mogen we hem aanvallen en stoppen we de loop
                    possibleAttackSquares.append(square)
                    break
                else:
                    # Als het van je eigen team is, kan je hem niet aanvallen en dus doen we niks.
                    break

        # Doe dit voor North West, South West en South East.
        for square in self.getAttackSquaresDiagNW():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                else:
                    break

        for square in self.getAttackSquaresDiagSW():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                else:
                    break

        for square in self.getAttackSquaresDiagSE():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                else:
                    break

        return possibleAttackSquares

    def getAttackSquaresDiagNE(self):
        # Haalt alle squares die NE (north east) van het ChessPiece zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase[0:8]
        temp = []

        try:
            for i in range(1, 8):
                if (int(row) + i > 8) or (alphabet[alphabet.find(column) + i] == "H"):
                    search = alphabet[alphabet.find(column) + i] + str(int(row) + i)
                    temp.append(search)
                    break
                else:
                    search = alphabet[alphabet.find(column) + i] + str(int(row) + i)
                    temp.append(search)
        except IndexError:
            pass

        for square in self.board.allSquares:
            for search in temp:
                if search in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getAttackSquaresDiagNW(self):
        # Haalt alle squares die NW (north west) van het ChessPiece zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase[0:8]
        temp = []

        try:
            for i in range(1, 8):
                if (int(row) + i > 8) or (alphabet[alphabet.find(column) - i] == "A"):
                    search = alphabet[alphabet.find(column) - i] + str(int(row) + i)
                    temp.append(search)
                    break
                else:
                    search = alphabet[alphabet.find(column) - i] + str(int(row) + i)
                    temp.append(search)
        except IndexError:
            pass

        for square in self.board.allSquares:
            for search in temp:
                if search in square.objectName():
                    possibleAttackSquares.insert(0, square)

        return possibleAttackSquares

    def getAttackSquaresDiagSW(self):
        # Haalt alle squares die NW (south west) van het ChessPiece zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase[0:8]
        temp = []

        try:
            for i in range(int(row) - 1, 0, -1):
                if alphabet[alphabet.find(column) + i - int(row)] == "A":
                    temp.append(alphabet[alphabet.find(column) + i - int(row)] + str(i))
                    break
                else:
                    temp.append(alphabet[alphabet.find(column) + i - int(row)] + str(i))
        except IndexError:
            pass

        for square in self.board.allSquares:
            for search in temp:
                if search in square.objectName():
                    possibleAttackSquares.insert(0, square)

        return possibleAttackSquares

    def getAttackSquaresDiagSE(self):
        # Haalt alle squares die SE (south east) van het ChessPiece zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase[0:8]
        temp = []

        try:
            for i in range(int(row) - 1, 0, -1):
                if alphabet[alphabet.find(column) + int(row) - i] == "H":
                    temp.append(alphabet[alphabet.find(column) + int(row) - i] + str(i))
                    break
                else:
                    temp.append(alphabet[alphabet.find(column) + int(row) - i] + str(i))
        except IndexError:
            pass

        for square in self.board.allSquares:
            for search in temp:
                if search in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def bishopLongdiagonal(self):
        # Returnt een boolean dat bepaalt of de bishop op de "long diagonal" zit of niet.

        # Dit is de diagonaal van links beneden naar rechts boven.
        for i in range(8):
            # Als de positie van de bishop op de long diagonal zit, return True
            if self.pos() == self.board.allSquares[0 + i * 9].pos():
                return True

        # Dit is de diagonaal van links boven naar rechts beneden.
        for i in range(8):
            if self.pos() == self.board.allSquares[7 + i * 7].pos():
                return True

        # Als ze er niet op zitten, dan return false.
        return False

    # De bishop is sterk wanneer je hem fianchetto. Als hij op de "long diagonal" zit, dan geven we hem extra punten.
    # Verder is de bishop ook erg actief als hij in het midden zit. Als hij aan de buitenkant ligt, dan geven we hem
    # minpunten.
    def getValue(self):
        bishopWeight = 30

        # Als de bishop op de long diagonal zit, geef ze extra punten.
        if self.bishopLongdiagonal() is True:
            bishopPositionWeight = 2

        # Als de bishop tussen C3 en F6 zitten, geven ze minder extra punten
        elif ("C" <= self.getPosition().objectName()[-2] <= "F") and (3 <= int(self.getPosition().objectName()[-1]) <= 6):
            bishopPositionWeight = 1

        # Als de positie van de bishop aan de buitenste kant ligt, dan krijgen ze min punten.
        elif (self.getPosition().objectName()[-2] == "A" or "H") or (
                    int(self.getPosition().objectName()[-1]) == 1 or 8):
            bishopPositionWeight = -1

        # Ze krijgen geen punten als ze op andere plekken zijn
        else:
            bishopPositionWeight = 0

        return bishopWeight + bishopPositionWeight