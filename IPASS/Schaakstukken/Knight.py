from myRepository.IPASS.Schaakstukken.Chesspiece import ChessPiece
import string


class Knight(ChessPiece):
    # De knight heeft een unieke patroon. Hij kan twee squares naar voren en dan naar links of rechts gaan.
    # Het maakt niet uit voor de knight of er iets staat op zijn pad.

    def getLegalMoves(self):
        # NOTE = Er is een veel efficientere manier om dit te doen. Helaas kwam ik hier later pas achter, dus voorlopig
        # laat ik het staan. Als ik nog tijd heb later, dan verbeter ik dit. (Het kan echt VEEL efficienter, alles is nu
        # brute force)

        # Return een lijst met squares die kunnen worden aangevallen door een knight
        possibleAttackSquares = []

        # Loop door alle squares die links van de knight zijn.
        for square in self.getAttackSquaresLeftSide():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                # Als er een stuk staat op die plek, dan moeten we kijken of het een witte stuk is of een zwarte stuk
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    # Als het van een andere team is, dan voegen we hem toe aan de mogelijke squares die we kunnen
                    # aanvallen.
                    possibleAttackSquares.append(square)

        # Loop door alle squares die boven de knight zijn.
        for square in self.getAttackSquaresAbove():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)

        # Loop door alle squares die rechts van de knight zijn.
        for square in self.getAttackSquaresRightSide():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)

        # Loop door alle squares die onder de knight zijn.
        for square in self.getAttackSquaresBelow():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)

        return possibleAttackSquares
    def getAttackSquaresLeftSide(self):
        # Zoekt naar de squares die kunnen worden aangevallen door de knight die links van hem staan
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase

        # Dit zijn de twee squares waar we naar zoeken
        searchSquares = [alphabet[alphabet.find(column) - 2] + str(int(row) - 1),
                         alphabet[alphabet.find(column) - 2] + str(int(row) + 1)]

        # Brute force zoek door alle squares heen.
        for square in self.board.allSquares:
            for searchSquare in searchSquares:
                if searchSquare in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getAttackSquaresAbove(self):
        # Zoekt naar de squares die kunnen worden aangevallen door de knight die boven hem staan
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase

        searchSquares = [alphabet[alphabet.find(column) - 1] + str(int(row) + 2),
                         alphabet[alphabet.find(column) + 1] + str(int(row) + 2)]

        for square in self.board.allSquares:
            for searchSquare in searchSquares:
                if searchSquare in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getAttackSquaresRightSide(self):
        # Zoekt naar de squares die kunnen worden aangevallen door de knight die rechts van hem staan
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase

        searchSquares = [alphabet[alphabet.find(column) + 2] + str(int(row) - 1),
                         alphabet[alphabet.find(column) + 2] + str(int(row) + 1)]


        for square in self.board.allSquares:
            for searchSquare in searchSquares:
                if searchSquare in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getAttackSquaresBelow(self):
        # Zoekt naar de squares die kunnen worden aangevallen door de knight die onder hem staan
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase

        searchSquares = [alphabet[alphabet.find(column) - 1] + str(int(row) - 2),
                         alphabet[alphabet.find(column) + 1] + str(int(row) - 2)]


        for square in self.board.allSquares:
            for searchSquare in searchSquares:
                if searchSquare in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getValue(self):
        # Return de waarde van een knight gebaseerd op de locatie van de knight en de waarde van de knight.
        knightWeight = 30

        # De knight kan het meest doen wanneer hij in het midden zit. Hier kan hij veel squares aanvallen.

        # Als de positie van de knight tussen D4 en E5 zitten, krijgen ze extra punten.
        if ("D" <= self.getPosition().objectName()[-2] <= "E") and (4 <= int(self.getPosition().objectName()[-1]) <= 5):
            knightPositionWeight = 2

        # Als de positie van de knight tussen C3 en F6 zitten, krijgen ze minder extra punten.
        elif ("C" <= self.getPosition().objectName()[-2] <= "F") and (3 <= int(self.getPosition().objectName()[-1]) <= 6):
            knightPositionWeight = 1

        # Als de positie van de knight aan de buitenste kant ligt, dan krijgen ze min punten.
        elif (self.getPosition().objectName()[-2] == "A" or "H") or (int(self.getPosition().objectName()[-1]) == 1 or 8):
            knightPositionWeight = -1

        # Op alle andere plekken de waarde van de knight 0
        else:
            knightPositionWeight = 0
        return knightWeight + knightPositionWeight