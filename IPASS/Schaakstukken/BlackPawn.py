from myRepository.IPASS.Schaakstukken.Chesspiece import ChessPiece
import string


class BlackPawn(ChessPiece):
    # Een black pawn kan naar beneden gaan en valt de twee squares aan die diagonaal onder de pawn staan.
    def getLegalMoves(self):
        # Return een lijst met squares waar de pawn naar toe kan gaan en kunnen aanvallen.
        possibleAttackSquares = []

        # Loop door alle squares boven de pawn.
        for square in self.getAttackSquaresAbove():
            # Als er niks voor hem staat kan de pawn vooruit
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            # Als er iets voor hem staat, dan mag de pawn er niet naartoe.
            else:
                break

        # Loop door de twee squares die diagonaal van de pawn zijn.
        for square in self.getAttackSquaresDiagonally():
            # Als er iets diagonaal van de pawn staat en het is van het andere team, dan kan de pawn hem aanvallen
            if square.containsPiece() != None and "white" in square.containsPiece().objectName():
                possibleAttackSquares.append(square)

        return possibleAttackSquares


    def getAttackSquaresDiagonally(self):
        # Return een lijst van squares die kunnen worden aangevallen. De squares zijn diagonaal van de pawn. De squares
        # kunnen alleen twee squares zijn die diagonaal van hem staan.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2:-1]
        possibleAttackSquares = []
        alphabet = string.ascii_letters

        left = alphabet[alphabet.find(column) - 1] + str(int(row) - 1)
        right = alphabet[alphabet.find(column) + 1] + str(int(row) - 1)
        for square in self.board.allSquares:
            if (left in square.objectName()) or (right in square.objectName()):
                possibleAttackSquares.append(square)
        return possibleAttackSquares

    def getAttackSquaresAbove(self):
        # Return de squares boven de pawn, waar de pawn naar toe kan.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []

        # Als de pawn nog niet heeft bewogen, kunnen we 2 stappen vooruit.
        if self.hasMoved == False:
            for square in self.board.allSquares:
                if ((column == square.objectName()[-2] and int(row) - 1 == int(square.objectName()[-1])) or
                        (column == square.objectName()[-2] and int(row) - 2 == int(square.objectName()[-1]))):
                    possibleAttackSquares.insert(0, square)
        # Anders kunnen ze alleen een stap vooruit
        else:
            for square in self.board.allSquares:
                if column == square.objectName()[-2] and int(row) - 1 == int(square.objectName()[-1]):
                    possibleAttackSquares.append(square)
        return possibleAttackSquares

    def checkIsolated(self):
        # Return een boolean dat bepaalt of de pawn geisoleerd is of niet.

        # Maak een lijst met huidige pawns
        currentPawns = []
        for piece in self.board.currentBlackPieces:
            if "pawn" in piece.objectName():
                currentPawns.append(piece)

        # Zet de huidige column van de pawn als currentColumn
        currentColumn = self.getPosition().objectName()[-2]

        # Zoek door alle pawns heen. Als ze naast de pawn zitten, dan is hij niet geisoleerd.
        for pawn in currentPawns:
            # Als er een pawn is dat naast hun staat, is hij niet geisoleerd
            if pawn.getPosition().objectName()[-2] == string.ascii_uppercase[string.ascii_uppercase.find(currentColumn) - 1]\
                    or pawn.getPosition().objectName()[-2] == string.ascii_uppercase[string.ascii_uppercase.find(currentColumn) + 1]:
                return False
        # Als ze door de hele loop zijn gegaan en ze kunnen geen pawn vinden dat naast hun staat, dan is hij geisoleerd
        return True

    def checkDoubledPawns(self):
        # Returnt een boolean als de pawn een deel is van een doubled pawns.
        # Een doubled pawn zijn twee pawns op dezelfde column.

        # Maak een lijst met huidige pawns
        currentPawns = []
        for piece in self.board.currentBlackPieces:
            if "pawn" in piece.objectName():
                currentPawns.append(piece)

        # Zet de huidige naam van de column van de pawn als currentColumn
        currentColumn = self.getPosition().objectName()[-2]

        # Loop door alle pawns
        for pawn in currentPawns:
            # Als de pawn op dezelfde column zit als een andere pawn, dan is hij doubled.
            if pawn.getPosition().objectName()[-2] == currentColumn and self != pawn:
                return True
        return False

    def getValue(self):
        blackPawnWeight = 10

        # Als de pawn bijna promoveert krijgt hij ook extra punten.
        if "2" == self.getPosition().objectName()[-1]:
            pawnPositionWeight = 5

        # Als de pawn tussen D4 en E5 zit, dan krijgt hij extra punten
        elif ("D" <= self.getPosition().objectName()[-2] <= "E") and (4 <= int(self.getPosition().objectName()[-1]) <= 5):
            pawnPositionWeight = 2



        # Op elke andere plek krijgen ze geen extra punten.
        else:
            pawnPositionWeight = 0

        # Als de pawn geisoleerd is dan krijgt hij -1 punt.
        if self.checkIsolated() is True:
            pawnPositionWeight -= 1

        # Als de pawn doubled is dan krijgt hij -1 punt.
        if self.checkDoubledPawns() is True:
            pawnPositionWeight -= 1

        return blackPawnWeight + pawnPositionWeight