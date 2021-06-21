from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtCore import QMimeData, Qt

import sys


# ChessPiece en Square zijn grotendeels gemaakt door:
# https://stackoverflow.com/questions/50232639/drag-and-drop-qlabels-with-pyqt5


class ChessPiece(QLabel):
    # Parent class voor alle schaakstukken
    def __init__(self, *args, board):
        QLabel.__init__(self, *args)
        self.setAcceptDrops(True)
        self.hasMoved = False
        self.board = board
        self.originalPosition = self.pos()

    def getOriginalPosition(self):
        return self.originalPosition

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        # Doe dit als een chesspiece op een chesspiece valt.

        if (self.board.turnCount % 2 == 0) and ("white" in self.board.clickedChessPiece.objectName()):

            # Hier checken we of een ChessPiece een andere ChessPiece mag aanvallen
            # Als de square in .getLegalMoves() zit, dan kunnen we hem aanvallen
            if self.getPosition() in self.board.clickedChessPiece.getLegalMoves():

                # We veranderen de positie van het object dat geclicked is.
                clickedPiecePreviousPosition = self.board.clickedChessPiece.pos()
                self.board.clickedChessPiece.move(self.pos())

                # Hier halen we het stuk dat wordt aangevallen weg. Ik heb meerdere manieren geprobeerd zoals gezegd op
                # websites zoals stackoverflow, maar het is mij niet gelukt. Daarom moet ik hem simpel weg verplaatsen
                # uit het scherm
                self.move(-100, -100)
                self.board.currentBlackPieces.remove(self)

                # Als de koning wordt aangevallen nadat de move wordt gedaan, dan is de move illegaal.
                # Dit is niet een goede manier om te checken wat de legal moves zijn van de koning, want dan kunnen we
                # niet checken voor checkmate. Maar ik wist niet hoe je moest checken wat de legal moves zijn als de
                # koning in check was.
                if len(self.board.whitePieces[-1].underAttack()) != 0:
                    self.move(self.board.clickedChessPiece.pos())
                    self.board.clickedChessPiece.move(clickedPiecePreviousPosition)
                    print("King would be under attack!")
                    self.board.currentBlackPieces.append(self)

                # Als de koning niet wordt aangevallen nadat de move wordt gedaan, dan updaten we de evaluatie en
                # geven we de beurt aan de andere persoon.
                else:
                    self.board.clickedChessPiece.hasMoved = True
                    self.board.turnCount += 1
                    self.board.evaluationBar.evaluateBoard()

                    if self.board.blackPieces[-1].checkForCheckmate() is True:
                        print("Game over! Black lost!")
                    # Als de koning heeft bewogen, dan heeft hij de castleRights verloren.
                    if "king" in self.board.clickedChessPiece.objectName():
                        self.castleRights = False
                event.acceptProposedAction()

            else:
                # Als een chesspiece niet naar een square kan, dan betekent het dat hij daar niet naar toe kan gaan,
                # want die square zit niet in .getLegalMoves()
                print(self.board.clickedChessPiece.objectName() + " can't go to " + self.objectName())

        # Precies hetzelfde hier, behalve dan voor zwart.
        elif (self.board.turnCount % 2 == 1) and ("black" in self.board.clickedChessPiece.objectName()):

            if self.getPosition() in self.board.clickedChessPiece.getLegalMoves():
                clickedPiecePreviousPosition = self.board.clickedChessPiece.pos()
                self.board.clickedChessPiece.move(self.pos())
                self.move(-100, -100)
                self.board.currentWhitePieces.remove(self)

                if len(self.board.blackPieces[-1].underAttack()) != 0:
                    self.move(self.board.clickedChessPiece.pos())
                    self.board.clickedChessPiece.move(clickedPiecePreviousPosition)
                    print("King would be under attack!")
                    self.board.currentWhitePieces.append(self)

                else:
                    self.board.clickedChessPiece.hasMoved = True
                    self.board.turnCount += 1
                    self.board.evaluationBar.evaluateBoard()

                    if self.board.whitePieces[-1].checkForCheckmate() is True:
                        print("Game over! White lost!")

                    if "king" in self.board.clickedChessPiece.objectName():
                        self.castleRights = False
                event.acceptProposedAction()

            else:
                print(self.board.clickedChessPiece.objectName() + " can't go to " + self.objectName())
        else:
            print("Het is niet jouw beurt!")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        # Dit gebeurt er als de muis beweegt en hij heeft geklikt op een chesspiece.

        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()

        # Zet het schaakstuk dat beweegt als clickedPieceObject.
        # Dit zullen we later gebruiken om te bepalen welke schaakstukken we moeten bewegen.

        self.board.clickedChessPiece = self

        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)

    def getPosition(self):
        # Return de square waar het schaakstuk op staat

        # Loop door alle squares om te kijken of de posities hetzelfde zijn.
        for square in self.board.allSquares:
            if self.pos() == square.pos():
                return square