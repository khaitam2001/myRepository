from myRepository.IPASS.Schaakstukken.Chesspiece import ChessPiece
from PyQt5.QtWidgets import QLabel
import string
import time


class King(ChessPiece):
    def __init__(self, *args, board):
        QLabel.__init__(self, *args)
        self.setAcceptDrops(True)
        self.hasMoved = False
        self.castleRights = True
        self.hasCastled = False
        self.board = board
        self.originalPosition = self.pos()

    # De koning is het meest belangrijke stuk. De koning kan 1 square om zich heen bewegen en heeft toegang tot
    # de move "castling". Hier zitten wel restricties op.
    def getLegalMoves(self):

        # Return een lijst met squares waar een koning naartoe kan gaan.
        possibleAttackSquares = []

        # Loop door de squares rond de koning.
        for square in self.getSquaresAroundPiece():

            # Als de square geen schaakstuk bevat, dan checken we of die square wordt aangevallen door een schaakstuk
            # van het ander team. Als dat true is, dan kunnen we er niet naartoe.
            if square.containsPiece() == None:
                attackingPieces = []
                if self.objectName()[0:5] == "white":
                    # Check hier of zwarte stukken naar die square kunnen gaan.
                    for piece in self.board.currentBlackPieces[:-1]:
                        # Check niet de koning, want anders krijg je infinite loop.
                        if "king" not in piece.objectName():
                            # De legal moves van pawn zijn plekken waar de pawn naartoe kunnen, maar niet per se kunnen
                            # aanvallen. Hiervoor moet ik helaas dus een if voor gebruiken.
                            if "pawn" in piece.objectName():
                                if square in piece.getAttackSquaresDiagonally():
                                    attackingPieces.append(piece)
                                    break
                            elif square in piece.getLegalMoves():
                                attackingPieces.append(piece)
                                break

                # Doe hetzelfde, maar dan checken we of de witte stukken het kunnen aanvallen.
                elif self.objectName()[0:5] == "black":
                    for piece in self.board.currentWhitePieces[:-1]:
                        if "king" not in piece.objectName():
                            if "pawn" in piece.objectName():
                                if square in piece.getAttackSquaresDiagonally():
                                    attackingPieces.append(piece)
                                    break
                            elif square in piece.getLegalMoves():
                                attackingPieces.append(piece)
                                break
                # Als er geen attackingpieces zijn, dan betekent het dat niemand het aanvalt.
                # De koning kan er dus dan naartoe.
                if len(attackingPieces) == 0:
                    possibleAttackSquares.append(square)

            # Als er wel een schaakstuk op die plek staat dan moeten we checken of het schaakstuk van ons is of niet
            else:
                # Als het stuk van een andere team is, dan kunnen we hem aanvallen.
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)

        # Check hier of castlelong mogelijk is.
        if self.castleLong() is not None:
            possibleAttackSquares.append(self.castleLong())

        # Check hier of castleshort mogelijk is.
        if self.castleShort() is not None:
            possibleAttackSquares.append(self.castleShort())


        return possibleAttackSquares

    def getSquaresAroundPiece(self):
        # Return een lijst met squares die om de koning heen zitten
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        alphabet = string.ascii_uppercase
        possibleAttackSquares = []

        squareNames = []
        for i in range(-1, 2):
            squareNames.append(alphabet[alphabet.find(column) + i] + str(int(row) - 1))
            squareNames.append(alphabet[alphabet.find(column) + i] + str(int(row)))
            squareNames.append(alphabet[alphabet.find(column) + i] + str(int(row) + 1))

        for square in self.board.allSquares:
            for name in squareNames:
                if name in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def castleLong(self):
        # Return een square, als castleLong een legal move is.

        # De koning mag niet hebben bewogen voor de castle
        if self.castleRights is True:
            # Condities voor een long castle:
            # 1. A1 is NIET leeg, 2. A1.hasMoved is False, B1 is leeg, 3. C1 is leeg, 4. D1 is leeg, en koning is wit.
            if self.board.allSquares[0].containsPiece() is not None:
                if ("white" in self.objectName()) and (self.board.allSquares[0].containsPiece().hasMoved is False) and \
                        (self.board.allSquares[8].containsPiece() is None) and (self.board.allSquares[16].containsPiece() is None) \
                        and (self.board.allSquares[24].containsPiece() is None):
                    return self.board.allSquares[16]

            # Precies dezelfde condities maar nu is het de 8ste rij. Dus B8, C8, D8 en koning is zwart.
            elif self.board.allSquares[7].containsPiece() is not None:
                if ("black" in self.objectName()) and (self.board.allSquares[7].containsPiece().hasMoved is False) and \
                        (self.board.allSquares[15].containsPiece() is None) and (self.board.allSquares[23].containsPiece() is None) \
                        and (self.board.allSquares[31].containsPiece() is None):
                    return self.board.allSquares[23]

    # Check of castleshort available is
    def castleShort(self):
        # Return een square, als castle short een legal move is.
        # De koning mag niet hebben bewogen voor de castle.
        if self.castleRights is True:
            # Condities voor een short castle:
            # 1. H1 is NIET leeg, 2. H1.hasMoved is False, G1 is leeg, 3. F1 is leeg en koning is wit.
            if self.board.allSquares[56].containsPiece() is not None:
                if ("white" in self.objectName()) and (self.board.allSquares[56].containsPiece().hasMoved is False) and \
                        (self.board.allSquares[48].containsPiece() is None) and (self.board.allSquares[40].containsPiece() is None):
                    return self.board.allSquares[48]

            # Precies dezelfde condities maar nu is het de 8ste rij. Dus H8, G8 en F1 en de koning is zwart.
            elif self.board.allSquares[63].containsPiece() is not None:
                if ("black" in self.objectName()) and (self.board.allSquares[63].containsPiece().hasMoved is False) and \
                        (self.board.allSquares[55].containsPiece() is None) and (self.board.allSquares[47].containsPiece() is None):
                    return self.board.allSquares[55]

    # Check of de koning wordt aangevallen en return de piece(s) dat de koning aanvalt.
    def underAttack(self):
        attackingPieces = []
        if "white" in self.objectName():
            for piece in self.board.currentBlackPieces:
                if "king" not in piece.objectName():
                    if self.getPosition() in piece.getLegalMoves():
                        attackingPieces.append(piece)
        elif "black" in self.objectName():
            for piece in self.board.currentWhitePieces:
                if "king" not in piece.objectName():
                    if self.getPosition() in piece.getLegalMoves():
                        attackingPieces.append(piece)
        return attackingPieces

    # De koning is het meest belangrijke schaakstuk op het boord. Daarom heeft hij zo'n hoge waarde. Een koning dat
    # veilig is, is meer waard dan een koning aan de andere kant van het boord.
    def getValue(self):
        kingWeight = 900

        # Doe dit als de koning zwart is.
        if "black" in self.objectName():

            # Voor elke rij dat de koning onder de begin rij is, wordt een een punt afgetrokken.
            row = int(self.getPosition().objectName()[-1])
            kingPositionWeight = 3 - (8 - row)

        elif "white" in self.objectName():

            # Voor elke rij dat de koning boven de beginrij is, wordt er een punt afgetrokken.
            row = int(self.getPosition().objectName()[-1])
            kingPositionWeight = 3 - row + 1

        # Check hier of castle is gedaan.
        if self.hasCastled is True:
            kingPositionWeight += 3

        # Check hier of castle rights verloren zijn
        elif self.castleRights is False and self.hasCastled is False:
            kingPositionWeight -= 4

        score = kingWeight + kingPositionWeight
        return score

    # Check of er een checkmate is of niet.
    def checkForCheckmate(self):
        # Brute force de check voor checkmate door alle moves te bekijken. Als alle moves zijn gedaan en geen een van
        # die moves stopt checkmate, dan is er checkmate.

        # Check of de king uberhaupt wordt aangevallen.
        if len(self.underAttack()) != 0:
            # Als het wit is, dan checken we voor alle legalMoves van wit.
            if "white" in self.objectName():
                # Loop door alle witte schaakstukken
                for piece in self.board.currentWhitePieces:
                    piecePreviousLocation = piece.pos()
                    # Kijk wat er gebeurt voor elke legal move.
                    for square in piece.getLegalMoves():
                        squareContainsPiece = False

                        # Check hier of er iets staat op die square.
                        if square.containsPiece() != None:

                            # Als er iets op staat, dan halen we hem weg
                            containedPiece = square.containsPiece()
                            squareContainsPiece = True
                            self.board.currentBlackPieces.remove(containedPiece)
                            containedPiece.move(-100, -100)

                        piece.move(square.pos())
                        # Als de koning nog steeds wordt aangevallen, breng dan dat stuk terug
                        if len(self.underAttack()) != 0:
                            if squareContainsPiece == True:
                                containedPiece.move(square.pos())
                                self.board.currentBlackPieces.append(containedPiece)
                            piece.move(piecePreviousLocation)
                        # Als de koning niet meer wordt aangevallen dan is er geen sprake van schaakmat.
                        else:
                            if squareContainsPiece == True:
                                containedPiece.move(square.pos())
                                self.board.currentBlackPieces.append(containedPiece)
                            piece.move(piecePreviousLocation)
                            return False

            # Precies hetzelfde hier, maar dan met zwarte schaakstukken
            elif "black" in self.objectName():
                for piece in self.board.currentBlackPieces:
                    piecePreviousLocation = piece.pos()
                    for square in piece.getLegalMoves():
                        squareContainsPiece = False

                        if square.containsPiece() != None:
                            # Als er iets op staat, dan halen we hem weg
                            containedPiece = square.containsPiece()
                            squareContainsPiece = True
                            self.board.currentWhitePieces.remove(containedPiece)
                            containedPiece.move(-100, -100)

                        piece.move(square.pos())
                        if len(self.underAttack()) != 0:
                            if squareContainsPiece == True:
                                containedPiece.move(square.pos())
                                self.board.currentWhitePieces.append(containedPiece)
                            piece.move(piecePreviousLocation)
                        else:
                            if squareContainsPiece == True:
                                containedPiece.move(square.pos())
                                self.board.currentWhitePieces.append(containedPiece)
                            piece.move(piecePreviousLocation)
                            return False
            # Als ze door de loops heen zijn gegaan en ze konden geen legal moves vinden, dan is het schaakmat.
            return True
        # Als de koning niet eens wordt aangevallen dan is er geen schaakmat.
        else:
            return False
