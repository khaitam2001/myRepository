from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtCore import QMimeData, Qt

import sys
import string

""" 
KNOWN BUGS OR MISSING FEATURES

1. Er is geen check for checkmate.

"""

# ChessPiece en Square zijn grotendeels gemaakt door https://stackoverflow.com/questions/50232639/drag-and-drop-qlabels-with-pyqt5


class ChessPiece(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.hasMoved = False

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        global turnCount
        temp = []

        if (turnCount % 2 == 0) and ("white" in clickedPieceObject.objectName()):
            # Hier checken we of een ChessPiece een andere ChessPiece mag aanvallen
            for square in clickedPieceObject.getLegalMoves():
                # Voeg alle squares toe aan temp die wij kunnen aanvallen.
                temp.append(square.objectName())
            if (self.getPosition().objectName() in temp):
                # Als de positie van dat ChessPiece in temp zit, dan kunnen we hem aanvallen. Anders niet.
                clickedPiecePreviousPosition = clickedPieceObject.pos()
                clickedPieceObject.move(self.pos())
                clickedPieceObject.hasMoved = True

                # Ik hebself.hide(), self.setParent(None) en andere methodes geprobeert om de chesspiece weg te
                # halen maar die werken niet. Daarom gebruik ik self.move om hem weg te halen van het scherm
                self.move(-100, -100)
                currentBlackPieces.remove(self)

                # Als de koning wordt aangevallen nadat de move wordt gedaan, dan is de move illegaal.
                if len(whitePieces[-1].underAttack()) != 0:
                    self.move(clickedPieceObject.pos())
                    clickedPieceObject.move(clickedPiecePreviousPosition)
                    print("King would be under attack!")
                    currentBlackPieces.add(self)
                else:
                    turnCount += 1
                event.acceptProposedAction()

            else:
                # Als dat niet kan, dan printen we dat het niet kan.
                print(clickedPieceObject.objectName() + " can't go to " + self.objectName())

        elif (turnCount % 2 == 1) and ("black" in clickedPieceObject.objectName()):
            for square in clickedPieceObject.getLegalMoves():
                temp.append(square.objectName())

            if (self.getPosition().objectName() in temp):
                clickedPiecePreviousPosition = clickedPieceObject.pos()
                clickedPieceObject.move(self.pos())
                clickedPieceObject.hasMoved = True
                self.move(-100, -100)
                currentWhitePieces.remove(self)

                if len(blackPieces[-1].underAttack()) != 0:
                    self.move(clickedPieceObject.pos())
                    clickedPieceObject.move(clickedPiecePreviousPosition)
                    print("King would be under attack!")
                    currentWhitePieces.add(self)
                else:
                    turnCount += 1
                event.acceptProposedAction()

            else:
                print(clickedPieceObject.objectName() + " can't go to " + self.objectName())
        else:
            print("Het is niet jouw beurt!")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.text())

        global clickedPieceObject
        clickedPieceObject = self

        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)

    def getPosition(self):
        global allSquares
        for square in allSquares:
            if self.pos() == square.pos():
                return square


class Square(QLabel):
    # Dit is de class voor alle squares. Bijvoorbeeld de square A1
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        global turnCount
        if (turnCount % 2 == 0) and ("white" in clickedPieceObject.objectName()):
            # Ik moest de rook ook verplaatsen met de koning wanneer de speler wou castlen.
            # ik wist niet hoe je dit beter moest doen.

            # Doe dit als castle long en witte koning
            if (("king" in clickedPieceObject.objectName()) and (allSquares[16] == self) and (clickedPieceObject.hasMoved is False)):
                clickedPieceObject.move(self.pos())
                clickedPieceObject.hasMoved = True
                whitePieces[8].move(allSquares[24].pos())
                event.acceptProposedAction()
                turnCount += 1

            # Doe dit als castle short en witte koning
            elif (("king" in clickedPieceObject.objectName()) and (allSquares[48] == self) and (
                    clickedPieceObject.hasMoved is False)):
                clickedPieceObject.move(self.pos())
                clickedPieceObject.hasMoved = True
                whitePieces[9].move(allSquares[40].pos())
                event.acceptProposedAction()
                turnCount += 1

            # Doe dit als de moves geen castle moves waren.
            elif (self in clickedPieceObject.getLegalMoves()):

                clickedPiecePreviousPosition = clickedPieceObject.pos()
                clickedPieceObject.move(self.pos())
                clickedPieceObject.hasMoved = True

                if len(whitePieces[-1].underAttack()) != 0:
                    clickedPieceObject.move(clickedPiecePreviousPosition)
                    print("King would be under attack!")
                else:
                    turnCount += 1
                event.acceptProposedAction()

            else:
                print(clickedPieceObject.objectName() + " can't go to " + self.objectName())

        elif (turnCount % 2 == 1) and ("black" in clickedPieceObject.objectName()):
            # Nog maals weet ik niet een betere manier om te castlen.

            # Doe dit als castle long en zwarte koning
            if (("king" in clickedPieceObject.objectName()) and (allSquares[23] == self) and (
                        clickedPieceObject.hasMoved is False)):
                clickedPieceObject.move(self.pos())
                clickedPieceObject.hasMoved = True
                blackPieces[8].move(allSquares[31].pos())
                event.acceptProposedAction()
                turnCount += 1

            # Doe dit als castle short en zwarte koning
            elif (("king" in clickedPieceObject.objectName()) and (allSquares[55] == self) and (
                    clickedPieceObject.hasMoved is False)):
                clickedPieceObject.move(self.pos())
                clickedPieceObject.hasMoved = True
                blackPieces[9].move(allSquares[47].pos())
                event.acceptProposedAction()
                turnCount += 1

            elif (self in clickedPieceObject.getLegalMoves()):
                clickedPiecePreviousPosition = clickedPieceObject.pos()
                clickedPieceObject.move(self.pos())
                clickedPieceObject.hasMoved = True
                event.acceptProposedAction()

                if len(blackPieces[-1].underAttack()) != 0:
                    clickedPieceObject.move(clickedPiecePreviousPosition)
                    print("King would be under attack!")
                else:
                    turnCount += 1

            else:
                print(clickedPieceObject.objectName() + " can't go to " + self.objectName())
        else:
            print("Het is niet jouw beurt!")



    def containsPiece(self):
        # Return een object dat op die square staat. Anders return niks
        allPieces = blackPieces + whitePieces
        for piece in allPieces:
            if piece.pos() == self.pos():
                return piece
        else:
            return None

    def whiteCastleLong(self):
        if ("white_king" in clickedPieceObject.objectName() and ("B1" in self.objectName())):
            allSquares[0].containsPiece().move()


class Knight(ChessPiece):
    def getLegalMoves(self):
        """ Return een lijst met squares die kunnen worden aangevallen door een knight"""
        possibleAttackSquares = []

        for square in self.getAttackSquaresLeftSide():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                # Als er een stuk staat op die plek, dan moeten we kijken of het een witte stuk is of een zwarte stuk
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    # Als het van een andere team is, dan voegen we hem toe aan de mogelijke squares die we kunnen
                    # aanvallen.
                    possibleAttackSquares.append(square)

        for square in self.getAttackSquaresAbove():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)

        for square in self.getAttackSquaresRightSide():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)

        for square in self.getAttackSquaresBelow():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getAttackSquaresLeftSide(self):
        # Zoekt naar de squares die kunnen worden aangevallen door de knight die links van hem staan
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase

        searchSquares = [alphabet[alphabet.find(column) - 2] + str(int(row) - 1),
                         alphabet[alphabet.find(column) - 2] + str(int(row) + 1)]

        for square in allSquares:
            for searchSquare in searchSquares:
                if searchSquare in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getAttackSquaresAbove(self):
        # Zoekt naar de squares die kunnen worden aangevallen door de knight die boven hem staan
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase

        searchSquares = [alphabet[alphabet.find(column) - 1] + str(int(row) + 2),
                         alphabet[alphabet.find(column) + 1] + str(int(row) + 2)]

        for square in allSquares:
            for searchSquare in searchSquares:
                if searchSquare in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getAttackSquaresRightSide(self):
        # Zoekt naar de squares die kunnen worden aangevallen door de knight die rechts van hem staan
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase

        searchSquares = [alphabet[alphabet.find(column) + 2] + str(int(row) - 1),
                         alphabet[alphabet.find(column) + 2] + str(int(row) + 1)]


        for square in allSquares:
            for searchSquare in searchSquares:
                if searchSquare in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getAttackSquaresBelow(self):
        # Zoekt naar de squares die kunnen worden aangevallen door de knight die onder hem staan
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase

        searchSquares = [alphabet[alphabet.find(column) - 1] + str(int(row) - 2),
                         alphabet[alphabet.find(column) + 1] + str(int(row) - 2)]


        for square in allSquares:
            for searchSquare in searchSquares:
                if searchSquare in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares


class Bishop(ChessPiece):
    def getLegalMoves(self):
        """ Return een lijst met squares die kunnen worden aangevallen door een bishop"""
        possibleAttackSquares = []

        for square in self.getAttackSquaresDiagNE():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                # Als er een stuk staat op die plek, dan moeten we kijken of het een witte stuk is of een zwarte stuk
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    # Als het van een andere team is, dan voegen we hem toe aan de mogelijke squares die we kunnen
                    # aanvallen.
                    possibleAttackSquares.append(square)
                    break
                else:
                    # Als het van je eigen team is, kan je hem niet aanvallen en dus doen we niks.
                    break

        for square in self.getAttackSquaresDiagNW():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                else:
                    break

        for square in self.getAttackSquaresDiagSW():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                else:
                    break

        for square in self.getAttackSquaresDiagSE():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    break
                else:
                    break

        return possibleAttackSquares

    def getAttackSquaresDiagNE(self):
        # Haalt alle squares die NE (north east) van het ChessPiece zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase[0:8]
        temp = []

        try:
            for i in range(1, 8):
                if (int(row) + i > 8) or (alphabet[alphabet.find(column) + i] == "H"):
                    search = alphabet[alphabet.find(column) + i] + str(int(row) + i)
                    temp.append(search)
                    break
                else:
                    search = alphabet[alphabet.find(column) + i] + str(int(row) + i)
                    temp.append(search)
        except IndexError:
            pass

        for square in allSquares:
            for search in temp:
                if search in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getAttackSquaresDiagNW(self):
        # Haalt alle squares die NW (north west) van het ChessPiece zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase[0:8]
        temp = []

        try:
            for i in range(1, 8):
                if (int(row) + i > 8) or (alphabet[alphabet.find(column) - i] == "A"):
                    search = alphabet[alphabet.find(column) - i] + str(int(row) + i)
                    temp.append(search)
                    break
                else:
                    search = alphabet[alphabet.find(column) - i] + str(int(row) + i)
                    temp.append(search)
        except IndexError:
            pass

        for square in allSquares:
            for search in temp:
                if search in square.objectName():
                    possibleAttackSquares.insert(0, square)

        return possibleAttackSquares

    def getAttackSquaresDiagSW(self):
        # Haalt alle squares die NW (south west) van het ChessPiece zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase[0:8]
        temp = []

        try:
            for i in range(int(row) - 1, 0, -1):
                if alphabet[alphabet.find(column) + i - int(row)] == "A":
                    temp.append(alphabet[alphabet.find(column) + i - int(row)] + str(i))
                    break
                else:
                    temp.append(alphabet[alphabet.find(column) + i - int(row)] + str(i))
        except IndexError:
            pass

        for square in allSquares:
            for search in temp:
                if search in square.objectName():
                    possibleAttackSquares.insert(0, square)

        return possibleAttackSquares

    def getAttackSquaresDiagSE(self):
        # Haalt alle squares die SE (south east) van het ChessPiece zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        alphabet = string.ascii_uppercase[0:8]
        temp = []

        try:
            for i in range(int(row) - 1, 0, -1):
                if alphabet[alphabet.find(column) + int(row) - i] == "H":
                    temp.append(alphabet[alphabet.find(column) + int(row) - i] + str(i))
                    break
                else:
                    temp.append(alphabet[alphabet.find(column) + int(row) - i] + str(i))
                    pass
        except IndexError:
            pass

        for square in allSquares:
            for search in temp:
                if search in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares


class Rook(ChessPiece):
    def getLegalMoves(self):
        """ Return een lijst met squares die kunnen worden aangevallen rook. """
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
        # Return een lijst met alle squares die onder het schaakstuk zitten..
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        for square in allSquares:
            if (column == square.objectName()[-2] and int(row) > int(square.objectName()[-1])):
                possibleAttackSquares.insert(0, square)
        return possibleAttackSquares

    def getAttackSquaresAbove(self):
        # Return een lijst met alle squares die boven het schaakstuk zitten..
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        for square in allSquares:
            if (column == square.objectName()[-2] and int(row) < int(square.objectName()[-1])):
                possibleAttackSquares.append(square)
        return possibleAttackSquares

    def getAttackSquaresRight(self):
        # Return een lijst met alle squares die rechts van het schaakstuk zitten..
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        for square in allSquares:
            if (column < square.objectName()[-2] and row == square.objectName()[-1]):
                possibleAttackSquares.append(square)
        return possibleAttackSquares

    def getAttackSquaresLeft(self):
        # Return een lijst met alle squares die links van het schaakstuk zitten..
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []
        for square in allSquares:
            if (column > square.objectName()[-2] and row == square.objectName()[-1]):
                possibleAttackSquares.insert(0, square)
        return possibleAttackSquares


class Queen(Rook, Bishop):
    def getLegalMoves(self):
        possibleAttackSquares = []

        # De queen kan bewegen net als een rook en een biship. Daarom gebruiken we hun methodes.

        for square in Rook.getLegalMoves(self):
            possibleAttackSquares.append(square)

        for square in Bishop.getLegalMoves(self):
            possibleAttackSquares.append(square)

        return possibleAttackSquares


class King(ChessPiece):
    def getLegalMoves(self):
        # Return een lijst met squares waar een koning naartoe kan gaan.
        possibleAttackSquares = []

        # Check hier voor legal moves rond de koning.
        for square in self.getSquaresAroundPiece():

            # Als de square geen schaakstuk bevat, dan checken we of die square wordt aangevallen door een schaakstuk
            # van het ander team. Als dat true is, dan kunnen we er niet naartoe.
            if square.containsPiece() == None:
                attackingPieces = []
                if self.objectName()[0:5] == "white":
                    for piece in currentBlackPieces[:-1]:
                        # Pawns kunnen sommige plekken aanvallen, maar dat is niet in getlegalMove(). Daarom moet er
                        # helaas deze if statement komen.
                        if "pawn" in piece.objectName():
                            if square in piece.getAttackSquaresDiagonally():
                                attackingPieces.append(piece)
                                break
                        elif square in piece.getLegalMoves():
                            attackingPieces.append(piece)
                            break



                elif self.objectName()[0:5] == "black":
                    for piece in currentWhitePieces[:-1]:
                        if square in piece.getLegalMoves():
                            attackingPieces.append(piece)
                            break
                        elif "pawn" in piece.objectName():
                            if square in piece.getAttackSquaresDiagonally():
                                attackingPieces.append(piece)
                                break

                if len(attackingPieces) == 0:
                    possibleAttackSquares.append(square)

            else:
                supportingPieces = []
                # Als het stuk van een andere team is, dan kunnen we hem aanvallen.
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)
                    # Helaas kan de koning nu wel iets aanvallen, dat verdedigt wordt door een ander schaakstuk.
                    # Dit komt omdat piece.legalMoves() niet squares toevoegd, waar schaakstukken opstaan van zijn eigen
                    # team.

        if self.castleLong() is not None:
            possibleAttackSquares.append(self.castleLong())

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

        for square in allSquares:
            for name in squareNames:
                if name in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def castleLong(self):
        # Return een square, als castleLong een legal move is.

        # Als de koning wit is en B1, C1, D1 zijn leeg EN white_rook_a.hasMoved en koning.hasMoved is False. Dan is
        # castle long een legal move.
        if self.hasMoved is False:
            if allSquares[0].containsPiece() is not None:
                if ("white" in self.objectName()) and (allSquares[0].containsPiece().hasMoved is False) and \
                        (allSquares[8].containsPiece() is None) and (allSquares[16].containsPiece() is None) \
                        and (allSquares[24].containsPiece() is None):
                    return allSquares[16]

        # Als de koning zwart is en B8, C8, D8 zijn leeg EN black_rook_a.hasMoved en koning.hasMoved is False. Dan is
        # castle short een legal move
            elif allSquares[7].containsPiece() is not None:
                if ("black" in self.objectName()) and (allSquares[7].containsPiece().hasMoved is False) and \
                        (allSquares[15].containsPiece() is None) and (allSquares[23].containsPiece() is None) \
                        and (allSquares[31].containsPiece() is None):
                    return allSquares[23]

    def castleShort(self):
        # Return een square, als castle short een legal move is.
        if self.hasMoved is False:
            if allSquares[56].containsPiece() is not None:
                if ("white" in self.objectName()) and (allSquares[56].containsPiece().hasMoved is False) and \
                        (allSquares[48].containsPiece() is None) and (allSquares[40].containsPiece() is None):
                    return allSquares[48]

            elif allSquares[63].containsPiece() is not None:
                if ("black" in self.objectName()) and (allSquares[63].containsPiece().hasMoved is False) and \
                        (allSquares[55].containsPiece() is None) and (allSquares[47].containsPiece() is None):
                    return allSquares[55]

    # Check of de koning wordt aangevallen en return de piece dat de koning aanvalt.
    def underAttack(self):
        attackingPieces = []
        if "white" in self.objectName():
            for piece in currentBlackPieces:
                if self.getPosition() in piece.getLegalMoves():
                    attackingPieces.append(piece)
        elif "black" in self.objectName():
            for piece in currentWhitePieces:
                if self.getPosition() in piece.getLegalMoves():
                    attackingPieces.append(piece)
        return attackingPieces

    def defendKing(self):
        # Return een lijst met schaakstukken dat een schaakstuk kan aanvallen die op het moment de koning aan het
        # aanvallen is
        attackPieces = []
        if "white" in self.objectName():
            for whitePiece in currentWhitePieces:
                for attackingPiece in self.underAttack():
                    if attackingPiece.getPosition() in whitePiece.getLegalMoves():
                        attackPieces.append(whitePiece)
        elif "black" in self.objectName():
            for blackPiece in currentBlackPieces:
                for attackingPiece in self.underAttack():
                    if attackingPiece.getPosition() in blackPiece.getLegalMoves():
                        attackPieces.append(blackPiece)
        return attackPieces


class WhitePawn(ChessPiece):
    def getLegalMoves(self):
        possibleAttackSquares = []

        for square in self.getAttackSquaresAbove():
            # Als er niks voor hem staat kan de pawn vooruit
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                break

        for square in self.getAttackSquaresDiagonally():
            # Als er iets op de squares zitten, dan kan de pawn hem aanvallen
            if square.containsPiece() != None and "black" in square.containsPiece().objectName():
                possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getAttackSquaresDiagonally(self):
        """ Return een lijst van squares die kunnen worden aangevallen. De squares zijn diagonaal van de pawn. De squares
        kunnen alleen twee squares zijn die diagonaal voor hem staan."""
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2:-1]
        possibleAttackSquares = []
        alphabet = string.ascii_letters

        left = alphabet[alphabet.find(column) - 1] + str(int(row) + 1)
        right = alphabet[alphabet.find(column) + 1] + str(int(row) + 1)
        for square in allSquares:
            if (left in square.objectName()) or (right in square.objectName()):
                possibleAttackSquares.append(square)

        return possibleAttackSquares


    def getAttackSquaresAbove(self):
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []

        if self.hasMoved == False:
            for square in allSquares:
                if ((column == square.objectName()[-2] and int(row) + 1 == int(square.objectName()[-1])) or
                        (column == square.objectName()[-2] and int(row) + 2 == int(square.objectName()[-1]))):
                    possibleAttackSquares.append(square)
        else:
            for square in allSquares:
                if column == square.objectName()[-2] and int(row) + 1 == int(square.objectName()[-1]):
                    possibleAttackSquares.append(square)
        return possibleAttackSquares

class BlackPawn(ChessPiece):
    def getLegalMoves(self):
        possibleAttackSquares = []


        for square in self.getAttackSquaresAbove():
            # Als er niks voor hem staat kan de pawn vooruit
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                break

        for square in self.getAttackSquaresDiagonally():
            # Als er iets op de squares zitten, dan kan de pawn hem aanvallen
            if square.containsPiece() != None and "white" in square.containsPiece().objectName():
                possibleAttackSquares.append(square)

        return possibleAttackSquares


    def getAttackSquaresDiagonally(self):
        """ Return een lijst van squares die kunnen worden aangevallen. De squares zijn diagonaal van de pawn. De squares
        kunnen alleen twee squares zijn die diagonaal voor hem staan."""
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2:-1]
        possibleAttackSquares = []
        alphabet = string.ascii_letters

        left = alphabet[alphabet.find(column) - 1] + str(int(row) - 1)
        right = alphabet[alphabet.find(column) + 1] + str(int(row) - 1)
        for square in allSquares:
            if (left in square.objectName()) or (right in square.objectName()):
                possibleAttackSquares.append(square)
        return possibleAttackSquares

    def getAttackSquaresAbove(self):
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []

        # Als ze op de eerste rij zitten, kunnen ze 2 stappen vooruit
        if self.hasMoved == False:
            for square in allSquares:
                if ((column == square.objectName()[-2] and int(row) - 1 == int(square.objectName()[-1])) or
                        (column == square.objectName()[-2] and int(row) - 2 == int(square.objectName()[-1]))):
                    possibleAttackSquares.insert(0, square)
        # Anders kunnen ze alleen een stap vooruit
        else:
            for square in allSquares:
                if column == square.objectName()[-2] and int(row) - 1 == int(square.objectName()[-1]):
                    possibleAttackSquares.append(square)
        return possibleAttackSquares


from PyQt5 import QtCore, QtGui, QtWidgets

# Bijna alles in UI_MAINWINDOW is gemaakt met de tool "Qt Designer"
# Ik heb alleen de klassen verandert van de schaakstukken.
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 820)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.squareA1 = Square(self.centralwidget)
        self.squareA1.setGeometry(QtCore.QRect(0, 700, 101, 101))
        self.squareA1.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareA1.setObjectName("squareA1")
        self.squareA2 = Square(self.centralwidget)
        self.squareA2.setGeometry(QtCore.QRect(0, 600, 101, 101))
        self.squareA2.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareA2.setObjectName("squareA2")
        self.squareA3 = Square(self.centralwidget)
        self.squareA3.setGeometry(QtCore.QRect(0, 500, 101, 101))
        self.squareA3.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareA3.setObjectName("squareA3")
        self.squareA4 = Square(self.centralwidget)
        self.squareA4.setGeometry(QtCore.QRect(0, 400, 101, 101))
        self.squareA4.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareA4.setObjectName("squareA4")
        self.squareA5 = Square(self.centralwidget)
        self.squareA5.setGeometry(QtCore.QRect(0, 300, 101, 101))
        self.squareA5.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareA5.setObjectName("squareA5")
        self.squareA6 = Square(self.centralwidget)
        self.squareA6.setGeometry(QtCore.QRect(0, 200, 101, 101))
        self.squareA6.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareA6.setObjectName("squareA6")
        self.squareA7 = Square(self.centralwidget)
        self.squareA7.setGeometry(QtCore.QRect(0, 100, 101, 101))
        self.squareA7.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareA7.setObjectName("squareA7")
        self.squareA8 = Square(self.centralwidget)
        self.squareA8.setGeometry(QtCore.QRect(0, 0, 101, 101))
        self.squareA8.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareA8.setObjectName("squareA8")
        self.aColumn = QtWidgets.QLabel(self.centralwidget)
        self.aColumn.setGeometry(QtCore.QRect(91, 780, 20, 21))
        self.aColumn.setObjectName("aColumn")
        self.squareB8 = Square(self.centralwidget)
        self.squareB8.setGeometry(QtCore.QRect(100, 0, 101, 101))
        self.squareB8.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareB8.setObjectName("squareB8")
        self.squareB3 = Square(self.centralwidget)
        self.squareB3.setGeometry(QtCore.QRect(100, 500, 101, 101))
        self.squareB3.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareB3.setObjectName("squareB3")
        self.squareB4 = Square(self.centralwidget)
        self.squareB4.setGeometry(QtCore.QRect(100, 400, 101, 101))
        self.squareB4.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareB4.setObjectName("squareB4")
        self.squareB2 = Square(self.centralwidget)
        self.squareB2.setGeometry(QtCore.QRect(100, 600, 101, 101))
        self.squareB2.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareB2.setObjectName("squareB2")
        self.squareB5 = Square(self.centralwidget)
        self.squareB5.setGeometry(QtCore.QRect(100, 300, 101, 101))
        self.squareB5.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareB5.setObjectName("squareB5")
        self.bColumn = QtWidgets.QLabel(self.centralwidget)
        self.bColumn.setGeometry(QtCore.QRect(190, 780, 21, 21))
        self.bColumn.setObjectName("bColumn")
        self.squareB6 = Square(self.centralwidget)
        self.squareB6.setGeometry(QtCore.QRect(100, 200, 101, 101))
        self.squareB6.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareB6.setObjectName("squareB6")
        self.squareB7 = Square(self.centralwidget)
        self.squareB7.setGeometry(QtCore.QRect(100, 100, 101, 101))
        self.squareB7.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareB7.setObjectName("squareB7")
        self.squareB1 = Square(self.centralwidget)
        self.squareB1.setGeometry(QtCore.QRect(100, 700, 101, 101))
        self.squareB1.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareB1.setObjectName("squareB1")
        self.squareC5 = Square(self.centralwidget)
        self.squareC5.setGeometry(QtCore.QRect(200, 300, 101, 101))
        self.squareC5.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareC5.setObjectName("squareC5")
        self.squareC4 = Square(self.centralwidget)
        self.squareC4.setGeometry(QtCore.QRect(200, 400, 101, 101))
        self.squareC4.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareC4.setObjectName("squareC4")
        self.squareC1 = Square(self.centralwidget)
        self.squareC1.setGeometry(QtCore.QRect(200, 700, 101, 101))
        self.squareC1.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareC1.setObjectName("squareC1")
        self.squareC3 = Square(self.centralwidget)
        self.squareC3.setGeometry(QtCore.QRect(200, 500, 101, 101))
        self.squareC3.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareC3.setObjectName("squareC3")
        self.squareC6 = Square(self.centralwidget)
        self.squareC6.setGeometry(QtCore.QRect(200, 200, 101, 101))
        self.squareC6.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareC6.setObjectName("squareC6")
        self.cColumn = QtWidgets.QLabel(self.centralwidget)
        self.cColumn.setGeometry(QtCore.QRect(290, 780, 20, 21))
        self.cColumn.setObjectName("cColumn")
        self.squareC7 = Square(self.centralwidget)
        self.squareC7.setGeometry(QtCore.QRect(200, 100, 101, 101))
        self.squareC7.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareC7.setObjectName("squareC7")
        self.squareC8 = Square(self.centralwidget)
        self.squareC8.setGeometry(QtCore.QRect(200, 0, 101, 101))
        self.squareC8.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareC8.setObjectName("squareC8")
        self.squareC2 = Square(self.centralwidget)
        self.squareC2.setGeometry(QtCore.QRect(200, 600, 101, 101))
        self.squareC2.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareC2.setObjectName("squareC2")
        self.squareD6 = Square(self.centralwidget)
        self.squareD6.setGeometry(QtCore.QRect(300, 200, 101, 101))
        self.squareD6.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareD6.setObjectName("squareD6")
        self.squareD7 = Square(self.centralwidget)
        self.squareD7.setGeometry(QtCore.QRect(300, 100, 101, 101))
        self.squareD7.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareD7.setObjectName("squareD7")
        self.squareD5 = Square(self.centralwidget)
        self.squareD5.setGeometry(QtCore.QRect(300, 300, 101, 101))
        self.squareD5.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareD5.setObjectName("squareD5")
        self.squareD1 = Square(self.centralwidget)
        self.squareD1.setGeometry(QtCore.QRect(300, 700, 101, 101))
        self.squareD1.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareD1.setObjectName("squareD1")
        self.squareD3 = Square(self.centralwidget)
        self.squareD3.setGeometry(QtCore.QRect(300, 500, 101, 101))
        self.squareD3.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareD3.setObjectName("squareD3")
        self.squareD4 = Square(self.centralwidget)
        self.squareD4.setGeometry(QtCore.QRect(300, 400, 101, 101))
        self.squareD4.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareD4.setObjectName("squareD4")
        self.squareD2 = Square(self.centralwidget)
        self.squareD2.setGeometry(QtCore.QRect(300, 600, 101, 101))
        self.squareD2.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareD2.setObjectName("squareD2")
        self.squareD8 = Square(self.centralwidget)
        self.squareD8.setGeometry(QtCore.QRect(300, 0, 101, 101))
        self.squareD8.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareD8.setObjectName("squareD8")
        self.dColumn = QtWidgets.QLabel(self.centralwidget)
        self.dColumn.setGeometry(QtCore.QRect(390, 780, 16, 21))
        self.dColumn.setObjectName("dColumn")
        self.squareE8 = Square(self.centralwidget)
        self.squareE8.setGeometry(QtCore.QRect(400, 0, 101, 101))
        self.squareE8.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareE8.setObjectName("squareE8")
        self.squareE2 = Square(self.centralwidget)
        self.squareE2.setGeometry(QtCore.QRect(400, 600, 101, 101))
        self.squareE2.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareE2.setObjectName("squareE2")
        self.squareE6 = Square(self.centralwidget)
        self.squareE6.setGeometry(QtCore.QRect(400, 200, 101, 101))
        self.squareE6.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareE6.setObjectName("squareE6")
        self.squareE7 = Square(self.centralwidget)
        self.squareE7.setGeometry(QtCore.QRect(400, 100, 101, 101))
        self.squareE7.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareE7.setObjectName("squareE7")
        self.squareE1 = Square(self.centralwidget)
        self.squareE1.setGeometry(QtCore.QRect(400, 700, 101, 101))
        self.squareE1.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareE1.setObjectName("squareE1")
        self.squareE3 = Square(self.centralwidget)
        self.squareE3.setGeometry(QtCore.QRect(400, 500, 101, 101))
        self.squareE3.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareE3.setObjectName("squareE3")
        self.squareE5 = Square(self.centralwidget)
        self.squareE5.setGeometry(QtCore.QRect(400, 300, 101, 101))
        self.squareE5.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareE5.setObjectName("squareE5")
        self.eColumn = QtWidgets.QLabel(self.centralwidget)
        self.eColumn.setGeometry(QtCore.QRect(490, 780, 20, 21))
        self.eColumn.setObjectName("eColumn")
        self.squareE4 = Square(self.centralwidget)
        self.squareE4.setGeometry(QtCore.QRect(400, 400, 101, 101))
        self.squareE4.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareE4.setObjectName("squareE4")
        self.squareF2 = Square(self.centralwidget)
        self.squareF2.setGeometry(QtCore.QRect(500, 600, 101, 101))
        self.squareF2.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareF2.setObjectName("squareF2")
        self.squareF6 = Square(self.centralwidget)
        self.squareF6.setGeometry(QtCore.QRect(500, 200, 101, 101))
        self.squareF6.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareF6.setObjectName("squareF6")
        self.squareF7 = Square(self.centralwidget)
        self.squareF7.setGeometry(QtCore.QRect(500, 100, 101, 101))
        self.squareF7.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareF7.setObjectName("squareF7")
        self.squareF5 = Square(self.centralwidget)
        self.squareF5.setGeometry(QtCore.QRect(500, 300, 101, 101))
        self.squareF5.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareF5.setObjectName("squareF5")
        self.squareF4 = Square(self.centralwidget)
        self.squareF4.setGeometry(QtCore.QRect(500, 400, 101, 101))
        self.squareF4.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareF4.setObjectName("squareF4")
        self.squareF1 = Square(self.centralwidget)
        self.squareF1.setGeometry(QtCore.QRect(500, 700, 101, 101))
        self.squareF1.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareF1.setObjectName("squareF1")
        self.squareF8 = Square(self.centralwidget)
        self.squareF8.setGeometry(QtCore.QRect(500, 0, 101, 101))
        self.squareF8.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareF8.setObjectName("squareF8")
        self.squareF3 = Square(self.centralwidget)
        self.squareF3.setGeometry(QtCore.QRect(500, 500, 101, 101))
        self.squareF3.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareF3.setObjectName("squareF3")
        self.fColumn = QtWidgets.QLabel(self.centralwidget)
        self.fColumn.setGeometry(QtCore.QRect(590, 780, 21, 21))
        self.fColumn.setObjectName("fColumn")
        self.squareG8 = Square(self.centralwidget)
        self.squareG8.setGeometry(QtCore.QRect(600, 0, 101, 101))
        self.squareG8.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareG8.setObjectName("squareG8")
        self.squareG4 = Square(self.centralwidget)
        self.squareG4.setGeometry(QtCore.QRect(600, 400, 101, 101))
        self.squareG4.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareG4.setObjectName("squareG4")
        self.squareG1 = Square(self.centralwidget)
        self.squareG1.setGeometry(QtCore.QRect(600, 700, 101, 101))
        self.squareG1.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareG1.setObjectName("squareG1")
        self.squareG5 = Square(self.centralwidget)
        self.squareG5.setGeometry(QtCore.QRect(600, 300, 101, 101))
        self.squareG5.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareG5.setObjectName("squareG5")
        self.squareG3 = Square(self.centralwidget)
        self.squareG3.setGeometry(QtCore.QRect(600, 500, 101, 101))
        self.squareG3.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareG3.setObjectName("squareG3")
        self.gColumn = QtWidgets.QLabel(self.centralwidget)
        self.gColumn.setGeometry(QtCore.QRect(690, 770, 21, 31))
        self.gColumn.setObjectName("gColumn")
        self.squareG2 = Square(self.centralwidget)
        self.squareG2.setGeometry(QtCore.QRect(600, 600, 101, 101))
        self.squareG2.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareG2.setObjectName("squareG2")
        self.squareG6 = Square(self.centralwidget)
        self.squareG6.setGeometry(QtCore.QRect(600, 200, 101, 101))
        self.squareG6.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareG6.setObjectName("squareG6")
        self.squareG7 = Square(self.centralwidget)
        self.squareG7.setGeometry(QtCore.QRect(600, 100, 101, 101))
        self.squareG7.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareG7.setObjectName("squareG7")
        self.squareH5 = Square(self.centralwidget)
        self.squareH5.setGeometry(QtCore.QRect(700, 300, 101, 101))
        self.squareH5.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareH5.setObjectName("squareH5")
        self.squareH6 = Square(self.centralwidget)
        self.squareH6.setGeometry(QtCore.QRect(700, 200, 101, 101))
        self.squareH6.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareH6.setObjectName("squareH6")
        self.squareH3 = Square(self.centralwidget)
        self.squareH3.setGeometry(QtCore.QRect(700, 500, 101, 101))
        self.squareH3.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareH3.setObjectName("squareH3")
        self.squareH8 = Square(self.centralwidget)
        self.squareH8.setGeometry(QtCore.QRect(700, 0, 101, 101))
        self.squareH8.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareH8.setObjectName("squareH8")
        self.squareH7 = Square(self.centralwidget)
        self.squareH7.setGeometry(QtCore.QRect(700, 100, 101, 101))
        self.squareH7.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareH7.setObjectName("squareH7")
        self.squareH1 = Square(self.centralwidget)
        self.squareH1.setGeometry(QtCore.QRect(700, 700, 101, 101))
        self.squareH1.setPixmap(QtGui.QPixmap("Images/white_square.png"))
        self.squareH1.setObjectName("squareH1")
        self.hColumn = QtWidgets.QLabel(self.centralwidget)
        self.hColumn.setGeometry(QtCore.QRect(790, 780, 21, 21))
        self.hColumn.setObjectName("hColumn")
        self.squareH2 = Square(self.centralwidget)
        self.squareH2.setGeometry(QtCore.QRect(700, 600, 101, 101))
        self.squareH2.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareH2.setObjectName("squareH2")
        self.squareH4 = Square(self.centralwidget)
        self.squareH4.setGeometry(QtCore.QRect(700, 400, 101, 101))
        self.squareH4.setPixmap(QtGui.QPixmap("Images/green_square.png"))
        self.squareH4.setObjectName("squareH4")
        self.row1 = QtWidgets.QLabel(self.centralwidget)
        self.row1.setGeometry(QtCore.QRect(0, 700, 20, 21))
        self.row1.setObjectName("row1")
        self.row2 = QtWidgets.QLabel(self.centralwidget)
        self.row2.setGeometry(QtCore.QRect(0, 600, 21, 21))
        self.row2.setObjectName("row2")
        self.row3 = QtWidgets.QLabel(self.centralwidget)
        self.row3.setGeometry(QtCore.QRect(0, 500, 20, 21))
        self.row3.setObjectName("row3")
        self.row4 = QtWidgets.QLabel(self.centralwidget)
        self.row4.setGeometry(QtCore.QRect(0, 400, 21, 21))
        self.row4.setObjectName("row4")
        self.row5 = QtWidgets.QLabel(self.centralwidget)
        self.row5.setGeometry(QtCore.QRect(0, 300, 20, 21))
        self.row5.setObjectName("row5")
        self.row6 = QtWidgets.QLabel(self.centralwidget)
        self.row6.setGeometry(QtCore.QRect(0, 200, 21, 21))
        self.row6.setObjectName("row6")
        self.row7 = QtWidgets.QLabel(self.centralwidget)
        self.row7.setGeometry(QtCore.QRect(0, 100, 21, 31))
        self.row7.setObjectName("row7")
        self.row8 = QtWidgets.QLabel(self.centralwidget)
        self.row8.setGeometry(QtCore.QRect(0, 0, 21, 21))
        self.row8.setObjectName("row8")
        self.white_pawn_a = WhitePawn(self.centralwidget)
        self.white_pawn_a.setGeometry(QtCore.QRect(0, 600, 101, 101))
        self.white_pawn_a.setPixmap(QtGui.QPixmap("Images/white_pawn.png"))
        self.white_pawn_a.setObjectName("white_pawn_a")
        self.white_pawn_b = WhitePawn(self.centralwidget)
        self.white_pawn_b.setGeometry(QtCore.QRect(100, 600, 101, 101))
        self.white_pawn_b.setPixmap(QtGui.QPixmap("Images/white_pawn.png"))
        self.white_pawn_b.setObjectName("white_pawn_b")
        self.white_pawn_c = WhitePawn(self.centralwidget)
        self.white_pawn_c.setGeometry(QtCore.QRect(200, 600, 101, 101))
        self.white_pawn_c.setPixmap(QtGui.QPixmap("Images/white_pawn.png"))
        self.white_pawn_c.setObjectName("white_pawn_c")
        self.white_pawn_d = WhitePawn(self.centralwidget)
        self.white_pawn_d.setGeometry(QtCore.QRect(300, 600, 101, 101))
        self.white_pawn_d.setPixmap(QtGui.QPixmap("Images/white_pawn.png"))
        self.white_pawn_d.setObjectName("white_pawn_d")
        self.white_pawn_e = WhitePawn(self.centralwidget)
        self.white_pawn_e.setGeometry(QtCore.QRect(400, 600, 101, 101))
        self.white_pawn_e.setPixmap(QtGui.QPixmap("Images/white_pawn.png"))
        self.white_pawn_e.setObjectName("white_pawn_e")
        self.white_pawn_f = WhitePawn(self.centralwidget)
        self.white_pawn_f.setGeometry(QtCore.QRect(500, 600, 101, 101))
        self.white_pawn_f.setPixmap(QtGui.QPixmap("Images/white_pawn.png"))
        self.white_pawn_f.setObjectName("white_pawn_f")
        self.white_pawn_g = WhitePawn(self.centralwidget)
        self.white_pawn_g.setGeometry(QtCore.QRect(600, 600, 101, 101))
        self.white_pawn_g.setPixmap(QtGui.QPixmap("Images/white_pawn.png"))
        self.white_pawn_g.setObjectName("white_pawn_g")
        self.white_pawn_h = WhitePawn(self.centralwidget)
        self.white_pawn_h.setGeometry(QtCore.QRect(700, 600, 101, 101))
        self.white_pawn_h.setPixmap(QtGui.QPixmap("Images/white_pawn.png"))
        self.white_pawn_h.setObjectName("white_pawn_h")
        self.white_rook_a = Rook(self.centralwidget)
        self.white_rook_a.setGeometry(QtCore.QRect(0, 700, 101, 101))
        self.white_rook_a.setPixmap(QtGui.QPixmap("Images/white_rook.png"))
        self.white_rook_a.setObjectName("white_rook_a")
        self.white_rook_h = Rook(self.centralwidget)
        self.white_rook_h.setGeometry(QtCore.QRect(700, 700, 101, 101))
        self.white_rook_h.setPixmap(QtGui.QPixmap("Images/white_rook.png"))
        self.white_rook_h.setObjectName("white_rook_h")
        self.white_knight_b = Knight(self.centralwidget)
        self.white_knight_b.setGeometry(QtCore.QRect(100, 700, 101, 101))
        self.white_knight_b.setPixmap(QtGui.QPixmap("Images/white_knight.png"))
        self.white_knight_b.setObjectName("white_knight_b")
        self.white_knight_g = Knight(self.centralwidget)
        self.white_knight_g.setGeometry(QtCore.QRect(600, 700, 101, 101))
        self.white_knight_g.setPixmap(QtGui.QPixmap("Images/white_knight.png"))
        self.white_knight_g.setObjectName("white_knight_g")
        self.white_bishop_c = Bishop(self.centralwidget)
        self.white_bishop_c.setGeometry(QtCore.QRect(200, 700, 101, 101))
        self.white_bishop_c.setPixmap(QtGui.QPixmap("Images/white_bishop.png"))
        self.white_bishop_c.setObjectName("white_bishop_c")
        self.white_bishop_f = Bishop(self.centralwidget)
        self.white_bishop_f.setGeometry(QtCore.QRect(500, 700, 101, 101))
        self.white_bishop_f.setPixmap(QtGui.QPixmap("Images/white_bishop.png"))
        self.white_bishop_f.setObjectName("white_bishop_f")
        self.white_queen = Queen(self.centralwidget)
        self.white_queen.setGeometry(QtCore.QRect(300, 700, 101, 101))
        self.white_queen.setPixmap(QtGui.QPixmap("Images/white_queen.png"))
        self.white_queen.setObjectName("white_queen")
        self.white_king = King(self.centralwidget)
        self.white_king.setGeometry(QtCore.QRect(400, 700, 101, 101))
        self.white_king.setPixmap(QtGui.QPixmap("Images/white_king.png"))
        self.white_king.setObjectName("white_king")
        self.black_pawn_a = BlackPawn(self.centralwidget)
        self.black_pawn_a.setGeometry(QtCore.QRect(0, 100, 101, 101))
        self.black_pawn_a.setPixmap(QtGui.QPixmap("Images/black_pawn.png"))
        self.black_pawn_a.setObjectName("black_pawn_a")
        self.black_pawn_b = BlackPawn(self.centralwidget)
        self.black_pawn_b.setGeometry(QtCore.QRect(100, 100, 101, 101))
        self.black_pawn_b.setPixmap(QtGui.QPixmap("Images/black_pawn.png"))
        self.black_pawn_b.setObjectName("black_pawn_b")
        self.black_pawn_c = BlackPawn(self.centralwidget)
        self.black_pawn_c.setGeometry(QtCore.QRect(200, 100, 101, 101))
        self.black_pawn_c.setPixmap(QtGui.QPixmap("Images/black_pawn.png"))
        self.black_pawn_c.setObjectName("black_pawn_c")
        self.black_pawn_d = BlackPawn(self.centralwidget)
        self.black_pawn_d.setGeometry(QtCore.QRect(300, 100, 101, 101))
        self.black_pawn_d.setPixmap(QtGui.QPixmap("Images/black_pawn.png"))
        self.black_pawn_d.setObjectName("black_pawn_d")
        self.black_pawn_e = BlackPawn(self.centralwidget)
        self.black_pawn_e.setGeometry(QtCore.QRect(400, 100, 101, 101))
        self.black_pawn_e.setPixmap(QtGui.QPixmap("Images/black_pawn.png"))
        self.black_pawn_e.setObjectName("black_pawn_e")
        self.black_pawn_f = BlackPawn(self.centralwidget)
        self.black_pawn_f.setGeometry(QtCore.QRect(500, 100, 101, 101))
        self.black_pawn_f.setPixmap(QtGui.QPixmap("Images/black_pawn.png"))
        self.black_pawn_f.setObjectName("black_pawn_f")
        self.black_pawn_g = BlackPawn(self.centralwidget)
        self.black_pawn_g.setGeometry(QtCore.QRect(600, 100, 101, 101))
        self.black_pawn_g.setPixmap(QtGui.QPixmap("Images/black_pawn.png"))
        self.black_pawn_g.setObjectName("black_pawn_g")
        self.black_pawn_h = BlackPawn(self.centralwidget)
        self.black_pawn_h.setGeometry(QtCore.QRect(700, 100, 101, 101))
        self.black_pawn_h.setPixmap(QtGui.QPixmap("Images/black_pawn.png"))
        self.black_pawn_h.setObjectName("black_pawn_h")
        self.black_rook_a = Rook(self.centralwidget)
        self.black_rook_a.setGeometry(QtCore.QRect(0, 0, 101, 101))
        self.black_rook_a.setPixmap(QtGui.QPixmap("Images/black_rook.png"))
        self.black_rook_a.setObjectName("black_rook_a")
        self.black_rook_h = Rook(self.centralwidget)
        self.black_rook_h.setGeometry(QtCore.QRect(700, 0, 101, 101))
        self.black_rook_h.setPixmap(QtGui.QPixmap("Images/black_rook.png"))
        self.black_rook_h.setObjectName("black_rook_h")
        self.black_knight_b = Knight(self.centralwidget)
        self.black_knight_b.setGeometry(QtCore.QRect(100, 0, 101, 101))
        self.black_knight_b.setPixmap(QtGui.QPixmap("Images/black_knight.png"))
        self.black_knight_b.setObjectName("black_knight_b")
        self.black_knight_g = Knight(self.centralwidget)
        self.black_knight_g.setGeometry(QtCore.QRect(600, 0, 101, 101))
        self.black_knight_g.setPixmap(QtGui.QPixmap("Images/black_knight.png"))
        self.black_knight_g.setObjectName("black_knight_g")
        self.black_bishop_c = Bishop(self.centralwidget)
        self.black_bishop_c.setGeometry(QtCore.QRect(200, 0, 101, 101))
        self.black_bishop_c.setPixmap(QtGui.QPixmap("Images/black_bishop.png"))
        self.black_bishop_c.setObjectName("black_bishop_c")
        self.black_bishop_f = Bishop(self.centralwidget)
        self.black_bishop_f.setGeometry(QtCore.QRect(500, 0, 101, 101))
        self.black_bishop_f.setPixmap(QtGui.QPixmap("Images/black_bishop.png"))
        self.black_bishop_f.setObjectName("black_bishop_f")
        self.black_queen = Queen(self.centralwidget)
        self.black_queen.setGeometry(QtCore.QRect(300, 0, 101, 101))
        self.black_queen.setPixmap(QtGui.QPixmap("Images/black_queen.png"))
        self.black_queen.setObjectName("black_queen")
        self.black_king = King(self.centralwidget)
        self.black_king.setGeometry(QtCore.QRect(400, 0, 101, 101))
        self.black_king.setPixmap(QtGui.QPixmap("Images/black_king.png"))
        self.black_king.setObjectName("black_king")
        self.squareB2.raise_()
        self.squareB8.raise_()
        self.squareB4.raise_()
        self.squareB3.raise_()
        self.squareA8.raise_()
        self.squareA2.raise_()
        self.squareA7.raise_()
        self.squareB1.raise_()
        self.squareA6.raise_()
        self.squareB7.raise_()
        self.squareB5.raise_()
        self.squareA3.raise_()
        self.squareB6.raise_()
        self.squareA5.raise_()
        self.squareA4.raise_()
        self.squareA1.raise_()
        self.aColumn.raise_()
        self.bColumn.raise_()
        self.squareC5.raise_()
        self.squareC4.raise_()
        self.squareC1.raise_()
        self.squareC3.raise_()
        self.squareC6.raise_()
        self.cColumn.raise_()
        self.squareC7.raise_()
        self.squareC8.raise_()
        self.squareC2.raise_()
        self.squareD6.raise_()
        self.squareD7.raise_()
        self.squareD5.raise_()
        self.squareD1.raise_()
        self.squareD3.raise_()
        self.squareD4.raise_()
        self.squareD2.raise_()
        self.squareD8.raise_()
        self.dColumn.raise_()
        self.squareE8.raise_()
        self.squareE2.raise_()
        self.squareE6.raise_()
        self.squareE7.raise_()
        self.squareE1.raise_()
        self.squareE3.raise_()
        self.squareE5.raise_()
        self.eColumn.raise_()
        self.squareE4.raise_()
        self.squareF2.raise_()
        self.squareF6.raise_()
        self.squareF7.raise_()
        self.squareF5.raise_()
        self.squareF4.raise_()
        self.squareF1.raise_()
        self.squareF8.raise_()
        self.squareF3.raise_()
        self.fColumn.raise_()
        self.squareG8.raise_()
        self.squareG4.raise_()
        self.squareG1.raise_()
        self.squareG5.raise_()
        self.squareG3.raise_()
        self.gColumn.raise_()
        self.squareG2.raise_()
        self.squareG6.raise_()
        self.squareG7.raise_()
        self.squareH5.raise_()
        self.squareH6.raise_()
        self.squareH3.raise_()
        self.squareH8.raise_()
        self.squareH7.raise_()
        self.squareH1.raise_()
        self.hColumn.raise_()
        self.squareH2.raise_()
        self.squareH4.raise_()
        self.row1.raise_()
        self.row2.raise_()
        self.row3.raise_()
        self.row4.raise_()
        self.row5.raise_()
        self.row6.raise_()
        self.row7.raise_()
        self.row8.raise_()
        self.white_pawn_a.raise_()
        self.white_pawn_b.raise_()
        self.white_pawn_c.raise_()
        self.white_pawn_d.raise_()
        self.white_pawn_e.raise_()
        self.white_pawn_f.raise_()
        self.white_pawn_g.raise_()
        self.white_pawn_h.raise_()
        self.white_rook_a.raise_()
        self.white_rook_h.raise_()
        self.white_knight_b.raise_()
        self.white_knight_g.raise_()
        self.white_bishop_c.raise_()
        self.white_bishop_f.raise_()
        self.white_queen.raise_()
        self.white_king.raise_()
        self.black_pawn_a.raise_()
        self.black_pawn_b.raise_()
        self.black_pawn_c.raise_()
        self.black_pawn_d.raise_()
        self.black_pawn_e.raise_()
        self.black_pawn_f.raise_()
        self.black_pawn_g.raise_()
        self.black_pawn_h.raise_()
        self.black_rook_a.raise_()
        self.black_rook_h.raise_()
        self.black_knight_b.raise_()
        self.black_knight_g.raise_()
        self.black_bishop_c.raise_()
        self.black_bishop_f.raise_()
        self.black_queen.raise_()
        self.black_king.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1193, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.aColumn.setText(_translate("MainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                        "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#ffffff;\">a</span></p></body></html>"))
        self.bColumn.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:14pt; color:#05a24b;\">b</span></p></body></html>"))
        self.cColumn.setText(_translate("MainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                        "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#ffffff;\">c</span></p></body></html>"))
        self.dColumn.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:14pt; color:#05a24b;\">d</span></p></body></html>"))
        self.eColumn.setText(_translate("MainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                        "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#ffffff;\">e</span></p></body></html>"))
        self.fColumn.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:14pt; color:#05a24b;\">f</span></p></body></html>"))
        self.gColumn.setText(_translate("MainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                        "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#ffffff;\">g</span></p></body></html>"))
        self.hColumn.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:14pt; color:#05a24b;\">h</span></p></body></html>"))
        self.row1.setText(_translate("MainWindow",
                                     "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                     "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                     "p, li { white-space: pre-wrap; }\n"
                                     "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#ffffff;\">1</span></p></body></html>"))
        self.row2.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-size:14pt; color:#05a24b;\">2</span></p></body></html>"))
        self.row3.setText(_translate("MainWindow",
                                     "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                     "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                     "p, li { white-space: pre-wrap; }\n"
                                     "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#ffffff;\">3</span></p></body></html>"))
        self.row4.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-size:14pt; color:#05a24b;\">4</span></p></body></html>"))
        self.row5.setText(_translate("MainWindow",
                                     "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                     "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                     "p, li { white-space: pre-wrap; }\n"
                                     "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#ffffff;\">5</span></p></body></html>"))
        self.row6.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-size:14pt; color:#05a24b;\">6</span></p></body></html>"))
        self.row7.setText(_translate("MainWindow",
                                     "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                     "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                     "p, li { white-space: pre-wrap; }\n"
                                     "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#ffffff;\">7</span></p></body></html>"))
        self.row8.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-size:14pt; color:#05a24b;\">8</span></p></body></html>"))

        # Ik weet niet hoe ik dit zou moeten doen zonder global

        global allSquares
        global blackPieces
        global whitePieces
        global turnCount
        global currentBlackPieces
        global currentWhitePieces

        allSquares = [self.squareA1, self.squareA2, self.squareA3, self.squareA4, self.squareA5, self.squareA6, self.squareA7, self.squareA8,
                      self.squareB1, self.squareB2, self.squareB3, self.squareB4, self.squareB5, self.squareB6, self.squareB7, self.squareB8,
                      self.squareC1, self.squareC2, self.squareC3, self.squareC4, self.squareC5, self.squareC6, self.squareC7, self.squareC8,
                      self.squareD1, self.squareD2, self.squareD3, self.squareD4, self.squareD5, self.squareD6, self.squareD7, self.squareD8,
                      self.squareE1, self.squareE2, self.squareE3, self.squareE4, self.squareE5, self.squareE6, self.squareE7, self.squareE8,
                      self.squareF1, self.squareF2, self.squareF3, self.squareF4, self.squareF5, self.squareF6, self.squareF7, self.squareF8,
                      self.squareG1, self.squareG2, self.squareG3, self.squareG4, self.squareG5, self.squareG6, self.squareG7, self.squareG8,
                      self.squareH1, self.squareH2, self.squareH3, self.squareH4, self.squareH5, self.squareH6, self.squareH7, self.squareH8]

        blackPieces = [self.black_pawn_a, self.black_pawn_b, self.black_pawn_c, self.black_pawn_d, self.black_pawn_e,
                     self.black_pawn_f, self.black_pawn_g, self.black_pawn_h, self.black_rook_a, self.black_rook_h,
                     self.black_knight_b, self.black_knight_g, self.black_bishop_c, self.black_bishop_f,
                     self.black_queen, self.black_king]

        whitePieces = [self.white_pawn_a, self.white_pawn_b, self.white_pawn_c, self.white_pawn_d, self.white_pawn_e,
                     self.white_pawn_f, self.white_pawn_g, self.white_pawn_h, self.white_rook_a, self.white_rook_h,
                     self.white_knight_b, self.white_knight_g, self.white_bishop_c, self.white_bishop_f,
                     self.white_queen, self.white_king]

        currentBlackPieces = blackPieces.copy()

        currentWhitePieces = whitePieces.copy()

        turnCount = 0






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())