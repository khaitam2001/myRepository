from PyQt5.QtWidgets import QPushButton


class ResetButton(QPushButton):
    def __init__(self, *args, board):
        QPushButton.__init__(self,  *args)
        self.board = board

    def setOriginalPosition(self):
        # Zet de originele posities van alle schaakstukken
        allPieces = self.board.whitePieces + self.board.blackPieces

        for piece in allPieces:
            piece.originalPosition = piece.pos()

    def resetBoard(self):
        # Reset de hele board.
        self.board.setBlackPieces(self.board.blackPieces.copy())
        self.board.setWhitePieces(self.board.whitePieces.copy())
        self.board.turnCount = 0
        allPieces = self.board.whitePieces + self.board.blackPieces

        for piece in allPieces:
            piece.move(piece.originalPosition)
            piece.hasMoved = False

            if "king" in piece.objectName():
                piece.castleRights = True
                piece.hasCastled = False
