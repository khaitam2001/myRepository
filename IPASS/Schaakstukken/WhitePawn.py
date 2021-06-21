from myRepository.IPASS.Schaakstukken.Chesspiece import ChessPiece
import string


class WhitePawn(ChessPiece):
    # Een white pawn kan naar boven gaan en valt de twee squares aan die diagonaal boven de pawn staan.
    def getLegalMoves(self):
        possibleAttackSquares = []

        # Loop door alle squares boven de pawn
        for square in self.getAttackSquaresAbove():
            # Als er niks voor hem staat kan de pawn vooruit
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                break

        # Loop door de twee squares die diagonaal van de pawn zijn.
        for square in self.getAttackSquaresDiagonally():
            # Als er iets op de squares zitten, dan kan de pawn hem aanvallen
            if square.containsPiece() != None and "black" in square.containsPiece().objectName():
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

        left = alphabet[alphabet.find(column) - 1] + str(int(row) + 1)
        right = alphabet[alphabet.find(column) + 1] + str(int(row) + 1)
        for square in self.board.allSquares:
            if (left in square.objectName()) or (right in square.objectName()):
                possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getAttackSquaresAbove(self):
        # Return squares die boven de pawn zitten waar de pawn naar toe zou kunnen.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []

        # Als de pawn nog niet beweegt heeft, dan mag hij 2 squares omhoog.
        if self.hasMoved == False:
            for square in self.board.allSquares:
                if ((column == square.objectName()[-2] and int(row) + 1 == int(square.objectName()[-1])) or
                        (column == square.objectName()[-2] and int(row) + 2 == int(square.objectName()[-1]))):
                    possibleAttackSquares.append(square)
        else:
            # Anders mag hij alleen 1 square omhoog
            for square in self.board.allSquares:
                if column == square.objectName()[-2] and int(row) + 1 == int(square.objectName()[-1]):
                    possibleAttackSquares.append(square)
        return possibleAttackSquares

    def checkIsolatedPawns(self):
        # Returnt een boolean dat bepaalt of de pawn geisoleerd is of niet.
        # Geisoleerde pawns zijn pawns die geen pawns naast hun hebben.

        # Maak een lijst met huidige pawns
        currentPawns = []
        for piece in self.board.currentWhitePieces:
            if "pawn" in piece.objectName():
                currentPawns.append(piece)

        # Zet de huidige naam van de column van de pawn als currentColumn
        currentColumn = self.getPosition().objectName()[-2]

        # Zoek door alle pawns heen. Als ze naast de pawn zitten, dan is hij niet geisoleerd.
        for pawn in currentPawns:
            # Als er een pawn naast de pawn staat, dan is hij niet geisoleerd
            if pawn.getPosition().objectName()[-2] == string.ascii_uppercase[string.ascii_uppercase.find(currentColumn) - 1]\
                    or pawn.getPosition().objectName()[-2] == string.ascii_uppercase[string.ascii_uppercase.find(currentColumn) + 1]:
                return False
        # Als ze door de hele loop zijn gegaan en ze kunnen geen pawn vinden dat naast hun staat, dan is hij geisoleerd
        return True

    def checkDoubledPawns(self):
        # Returnt een boolean gebaseerd op of de pawn een deel is van een paar doubled pawns.
        # Een doubled pawn zijn twee pawns op dezelfde column.

        # Maak een lijst met huidige pawns
        currentPawns = []
        for piece in self.board.currentWhitePieces:
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
        whitePawnWeight = 10

        # Als de pawn tussen D4 en E5 zit, dan krijgt hij extra punten
        if ("D" <= self.getPosition().objectName()[-2] <= "E") and (4 <= int(self.getPosition().objectName()[-1]) <= 5):
            pawnPositionWeight = 2
        # Als de pawn bijna promoveert krijgt hij ook extra punten.
        elif "7" == self.getPosition().objectName()[-1]:
            pawnPositionWeight = 5

        # Op elke andere plek krijgen ze geen extra punten.
        else:
            pawnPositionWeight = 0

        # Als de pawn geisoleerd is dan krijgt hij -1 punt.
        if self.checkIsolatedPawns() is True:
            pawnPositionWeight -= 1

        # Als de pawn doubled is dan krijgt hij -1 punt.
        if self.checkDoubledPawns() is True:
            pawnPositionWeight -= 1

        return whitePawnWeight + pawnPositionWeight