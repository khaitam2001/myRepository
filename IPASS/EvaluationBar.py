from PyQt5.QtWidgets import QLabel


class Evaluate(QLabel):
    def __init__(self, *args, board):
        QLabel.__init__(self, *args)
        self.board = board

    # Return de value van alle witte stukken
    def whitePieceValue(self):
        totalValue = 0
        for piece in self.board.currentWhitePieces:
            totalValue += piece.getValue()
        return totalValue

    # Return de value van alle zwarte stukken
    def blackPieceValue(self):
        totalValue = 0
        for piece in self.board.currentBlackPieces:
            totalValue += piece.getValue()
        return totalValue

    # Verander de text van de evaluation label in de huidige evaluation.
    def evaluateBoard(self):
        self.setText("Evaluation: " + str(round((self.whitePieceValue() - self.blackPieceValue()) * 0.1, 2)))