from myRepository.IPASS

class Rook(ChessPiece):
    def getLegalMoves(self, allSquares):
        """ Return een lijst met squares die kunnen worden aangevallen rook. """
        possibleAttackSquares = []

        # Als er niks onder hem staat dan kan de rook ernaar toe, totdat er wel iets staat
        for square in self.getAttackSquaresUnder(allSquares):
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
        for square in self.getAttackSquaresAbove(allSquares):
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                else:
                    break

        # Als er niks links van hem staat dan kan de rook ernaar toe, totdat er wel iets staat
        for square in self.getAttackSquaresLeft(allSquares):
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                else:
                    break

        # Als er niks rechts van hem staat dan kan de rook ernaar toe, totdat er wel iets staat
        for square in self.getAttackSquaresRight(allSquares):
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                else:
                    break

        return possibleAttackSquares


    def getAttackSquaresUnder(self, allSquares):
        # Return een lijst met alle squares die onder het schaakstuk zitten..
        currentSquare = self.getPosition()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        for square in allSquares:
            if (column == square.objectName()[-2] and int(row) > int(square.objectName()[-1])):
                possibleAttackSquares.insert(0, square)
        return possibleAttackSquares

    def getAttackSquaresAbove(self, allSquares):
        # Return een lijst met alle squares die boven het schaakstuk zitten..
        currentSquare = self.getPosition()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        for square in allSquares:
            if (column == square.objectName()[-2] and int(row) < int(square.objectName()[-1])):
                possibleAttackSquares.append(square)
        return possibleAttackSquares

    def getAttackSquaresRight(self, allSquares):
        # Return een lijst met alle squares die rechts van het schaakstuk zitten..
        currentSquare = self.getPosition()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        for square in allSquares:
            if (column < square.objectName()[-2] and row == square.objectName()[-1]):
                possibleAttackSquares.append(square)
        return possibleAttackSquares

    def getAttackSquaresLeft(self, allSquares):
        # Return een lijst met alle squares die links van het schaakstuk zitten..
        currentSquare = self.getPosition()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        for square in allSquares:
            if (column > square.objectName()[-2] and row == square.objectName()[-1]):
                possibleAttackSquares.insert(0, square)
        return possibleAttackSquares