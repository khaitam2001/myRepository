from PyQt5.QtWidgets import QLabel
import sys


# ChessPiece en Square zijn grotendeels gemaakt door:
# https://stackoverflow.com/questions/50232639/drag-and-drop-qlabels-with-pyqt5


class Square(QLabel):
    # Dit is de class voor alle squares. Bijvoorbeeld de square A1
    def __init__(self, *args, board):
        QLabel.__init__(self, *args)
        self.setAcceptDrops(True)
        self.board = board

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        # Dit gebeurt er als er iets wordt gedropt op een square.

        # Check wiens beurt het is en welke kleur wordt bewogen.
        if (self.board.turnCount % 2 == 0) and ("white" in self.board.clickedChessPiece.objectName()):

            # We hebben hier twee if statements voor de castle. Dit komt omdat ik ook de rook moest bewegen wanneer de
            # koning wou castlen. Ik wist niet een betere manier om dit te doen.

            # Doe dit als castle long en witte koning
            if ("king" in self.board.clickedChessPiece.objectName()) and (self.board.allSquares[16] == self) and \
                    (self.board.clickedChessPiece.hasMoved is False):
                self.board.clickedChessPiece.move(self.pos())
                self.board.clickedChessPiece.hasMoved = True
                self.board.whitePieces[8].move(self.board.allSquares[24].pos())
                event.acceptProposedAction()
                self.board.turnCount += 1
                self.board.clickedChessPiece.hasCastled = True
                self.board.evaluationBar.evaluateBoard()

                # Check hier voor checkmate
                if self.board.blackPieces[-1].checkForCheckmate() is True:
                    print("Game over! Black lost!")
                    sys.exit()

            # Doe dit als castle short en witte koning
            elif (("king" in self.board.clickedChessPiece.objectName()) and (self.board.allSquares[48] == self)
                  and (self.board.clickedChessPiece.hasMoved is False)):
                self.board.clickedChessPiece.move(self.pos())
                self.board.clickedChessPiece.hasMoved = True
                self.board.whitePieces[9].move(self.board.allSquares[40].pos())
                event.acceptProposedAction()
                self.board.turnCount += 1
                self.board.clickedChessPiece.hasCastled = True
                self.board.evaluationBar.evaluateBoard()
                if self.board.blackPieces[-1].checkForCheckmate() is True:
                    print("Game over! Black lost!")
                    sys.exit()

            # Doe dit als de moves geen castle moves waren.
            # Check hier ook of de square in legalMoves zit.
            elif (self in self.board.clickedChessPiece.getLegalMoves()):

                # Onthoud de positie van een chesspiece voordat hij wordt bewogen.
                clickedPiecePreviousPosition = self.board.clickedChessPiece.pos()
                self.board.clickedChessPiece.move(self.pos())

                # Als de koning wordt aangevallen, nadat het stuk heeft bewogen, dan betekent het dat die move niet mag.
                if len(self.board.whitePieces[-1].underAttack()) != 0:
                    self.board.clickedChessPiece.move(clickedPiecePreviousPosition)
                    print("King would be under attack!")

                # Als de koning niet wordt aangevallen, dan is de move legaal en verzetten we het schaakstuk.
                else:
                    self.board.clickedChessPiece.hasMoved = True
                    self.board.turnCount += 1

                    # Als het de koning is, dan zeggen we dat hij niet meer mag castlen.
                    if "king" in self.board.clickedChessPiece.objectName():
                        self.board.clickedChessPiece.castleRights = False

                    # Update de evaluatie
                    self.board.evaluationBar.evaluateBoard()

                    # Check hier of het schaakmat is.
                    if self.board.blackPieces[-1].checkForCheckmate() is True:
                        print("Game over! Black lost!")
                        sys.exit()
                event.acceptProposedAction()
            else:
                print(self.board.clickedChessPiece.objectName() + " can't go to " + self.objectName())

        # Dit is precies hetzelfde, maar dan met zwart.
        elif (self.board.turnCount % 2 == 1) and ("black" in self.board.clickedChessPiece.objectName()):
            # Nog maals weet ik niet een betere manier om te castlen.

            # Doe dit als castle long en zwarte koning
            if (("king" in self.board.clickedChessPiece.objectName()) and (self.board.allSquares[23] == self) and (
                        self.board.clickedChessPiece.hasMoved is False)):
                self.board.clickedChessPiece.move(self.pos())
                self.board.clickedChessPiece.hasMoved = True
                self.board.blackPieces[8].move(self.board.allSquares[31].pos())
                event.acceptProposedAction()
                self.board.turnCount += 1
                self.board.clickedChessPiece.hasCastled = True
                self.board.evaluationBar.evaluateBoard()
                # Check hier voor checkmate
                if self.board.whitePieces[-1].checkForCheckmate() is True:
                    print("Game over! White lost!")
                    sys.exit()

            # Doe dit als castle short en zwarte koning
            elif (("king" in self.board.clickedChessPiece.objectName()) and (self.board.allSquares[55] == self) and (
                    self.board.clickedChessPiece.hasMoved is False)):
                self.board.clickedChessPiece.move(self.pos())
                self.board.clickedChessPiece.hasMoved = True
                self.board.blackPieces[9].move(self.board.allSquares[47].pos())
                event.acceptProposedAction()
                self.board.turnCount += 1
                self.board.clickedChessPiece.hasCastled = True
                self.board.evaluationBar.evaluateBoard()
                if self.board.whitePieces[-1].checkForCheckmate() is True:
                    print("Game over! White lost!")
                    sys.exit()

            elif (self in self.board.clickedChessPiece.getLegalMoves()):
                clickedPiecePreviousPosition = self.board.clickedChessPiece.pos()
                self.board.clickedChessPiece.move(self.pos())
                event.acceptProposedAction()

                if len(self.board.blackPieces[-1].underAttack()) != 0:
                    self.board.clickedChessPiece.move(clickedPiecePreviousPosition)
                    print("King would be under attack!")
                else:
                    self.board.clickedChessPiece.hasMoved = True
                    self.board.turnCount += 1
                    if "king" in self.board.clickedChessPiece.objectName():
                        self.board.clickedChessPiece.castleRights = False
                    self.board.evaluationBar.evaluateBoard()
                    if self.board.whitePieces[-1].checkForCheckmate() is True:
                        print("Game over! White lost!")
                        sys.exit()

            else:
                print(self.board.clickedChessPiece.objectName() + " can't go to " + self.objectName())

        else:
            print("Het is niet jouw beurt!")

    def containsPiece(self):
        # Return een object dat op die square staat. Anders return niks
        allPieces = self.board.blackPieces + self.board.whitePieces
        for piece in allPieces:
            if piece.pos() == self.pos():
                return piece
        return None