from myRepository.IPASS.Schaakstukken.Chesspiece import ChessPiece


class Rook(ChessPiece):
    def getLegalMoves(self):
        # Return een lijst met squares die kunnen worden aangevallen door de rook.
        possibleAttackSquares = []

        # Als er niks onder hem staat dan kan de rook ernaar toe, totdat er wel iets staat
        for square in self.getAttackSquaresUnder():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                # Als het stuk van een andere team is, dan kunnen we hem aanvallen.
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                # Anders doen we niks en stoppen we de loop
                else:
                    break
        # Als er niks boven hem staat dan kan de rook ernaar toe, totdat er wel iets staat
        for square in self.getAttackSquaresAbove():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                else:
                    break

        # Als er niks links van hem staat dan kan de rook ernaar toe, totdat er wel iets staat
        for square in self.getAttackSquaresLeft():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                else:
                    break

        # Als er niks rechts van hem staat dan kan de rook ernaar toe, totdat er wel iets staat
        for square in self.getAttackSquaresRight():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                else:
                    break

        return possibleAttackSquares


    def getAttackSquaresUnder(self):
        # Return een lijst met alle squares die onder het schaakstuk zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2]
        possibleAttackSquares = []
        for square in self.board.allSquares:
            if (column == square.objectName()[-2] and int(row) > int(square.objectName()[-1])):
                possibleAttackSquares.insert(0, square)
        return possibleAttackSquares

    def getAttackSquaresAbove(self):
        # Return een lijst met alle squares die boven het schaakstuk zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2]
        possibleAttackSquares = []
        for square in self.board.allSquares:
            if (column == square.objectName()[-2] and int(row) < int(square.objectName()[-1])):
                possibleAttackSquares.append(square)
        return possibleAttackSquares

    def getAttackSquaresRight(self):
        # Return een lijst met alle squares die rechts van het schaakstuk zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2]
        possibleAttackSquares = []
        for square in self.board.allSquares:
            if (column < square.objectName()[-2] and row == square.objectName()[-1]):
                possibleAttackSquares.append(square)
        return possibleAttackSquares

    def getAttackSquaresLeft(self):
        # Return een lijst met alle squares die links van het schaakstuk zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2]
        possibleAttackSquares = []
        for square in self.board.allSquares:
            if (column > square.objectName()[-2] and row == square.objectName()[-1]):
                possibleAttackSquares.insert(0, square)
        return possibleAttackSquares

    def openFile(self):
        # Return een boolean gebaseerd op of de rook op een openFile is of niet.
        # Een open file is een column zonder pawns.
        column = self.getPosition().objectName()[-2]
        # Loop door alle squares
        for square in self.board.allSquares:
            # Als de square dezelfde column is als de column van de rook dan checken we of er een pawn is.
            if column == square.objectName()[-2]:
                # Als het schaakstuk niks bevat dan checken we niks verder
                if square.containsPiece() is not None:
                    # Als het wel iets bevat kijken of we het een pawn is.
                    if ("pawn" in square.containsPiece().objectName()):
                            return False
        return True

    def protectingPastPawn(self):
        # Returnt een boolean gebaseerd op of de rook een past pawn aan het beschermen is.
        currentColumn = self.getPosition().objectName()[-2]

        # Als de rook wit is, dan moeten we checken of er een pawn staat op de 7de rij EN we moeten checken of de rook
        # er achter staat.
        if "white" in self.objectName():
            for square in self.board.allSquares:
                # Zoek naar de square met dezelfde column en de rij 7
                if square.objectName()[-2] == currentColumn and square.objectName()[-1] == "7" and square.containsPiece() is not None:
                    if "white_pawn" in square.containsPiece().objectName() and int(self.getPosition().objectName()[-1]) < 7:
                        return True
                    else:
                        break

        elif "black" in self.objectName():
            for square in self.board.allSquares:
                # Zoek naar de square met dezelfde column en de rij 1
                if square.objectName()[-2] == currentColumn and square.objectName()[-1] == "2" and square.containsPiece() is not None:
                    if "black_pawn" in square.containsPiece().objectName() and int(self.getPosition().objectName()[-1]) > 2:
                        return True
                    else:
                        break
        return False

    def getValue(self):
        rookWeight = 50
        rookPositionWeight = 0

        # Als de rook op de 7de rij staat of de 2de rij, dan krijgt hij extra punten
        if "white" in self.objectName():
            if self.getPosition().objectName()[-1] == "7":
                rookPositionWeight += 4
        elif "black" in self.objectName():
            if self.getPosition().objectName()[-1] == "2":
                rookPositionWeight += 4

        # Als de rook op een open file staat, dan krijgt hij +3 punten
        elif self.openFile() is True:
            rookPositionWeight += 3

        elif self.protectingPastPawn() is True:
            rookPositionWeight += 5

        return rookWeight + rookPositionWeight