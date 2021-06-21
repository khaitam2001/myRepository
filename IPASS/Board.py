class Board():
    # Een class om alle relevante informatie op te slaan.
    def __init__(self):
        self.allSquares = []
        self.whitePieces = []
        self.blackPieces = []
        self.currentWhitePieces = []
        self.currentBlackPieces = []
        self.turnCount = 0
        self.evaluationBar = 0
        self.clickedChessPiece = 0

    def setAllSquares(self, allSquares):
        self.allSquares = allSquares

    def setWhitePieces(self, whitePieces):
        self.whitePieces = whitePieces.copy()
        self.currentWhitePieces = whitePieces.copy()

    def setBlackPieces(self, blackPieces):
        self.blackPieces = blackPieces.copy()
        self.currentBlackPieces = blackPieces.copy()

    def setEvalBar(self, evaluationBar):
        self.evaluationBar = evaluationBar

    def setClickedChessPiece(self, chesspiece):
        self.clickedChessPiece = chesspiece