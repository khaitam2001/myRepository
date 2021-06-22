from myRepository.IPASS.Schaakstukken.Rook import Rook
from myRepository.IPASS.Schaakstukken.Bishop import Bishop


class Queen(Rook, Bishop):
    def getLegalMoves(self):
        possibleAttackSquares = []

        # De queen kan bewegen net als een rook en een bishop. Daarom gebruiken we hun methodes.

        for square in Rook.getLegalMoves(self):
            possibleAttackSquares.append(square)

        for square in Bishop.getLegalMoves(self):
            possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getValue(self):
        # Return de waarde van het schaakstuk
        queenWeight = 90
        queenPositionWeight = 0

        # Als er een knight en queen bestaan, dan krijgt de queen +2 punten.
        if "white" in self.objectName():
            for piece in self.board.currentWhitePieces:
                if "knight" in piece.objectName():
                    queenPositionWeight += 2
                    break

        elif "black" in self.objectName():
            for piece in self.board.currentBlackPieces:
                if "knight" in piece.objectName():
                    queenPositionWeight += 2
                    break

        return queenWeight + queenPositionWeight