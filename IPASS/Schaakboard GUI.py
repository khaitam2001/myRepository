from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtCore import QMimeData, Qt

import sys
import string

""" 
KNOWN BUGS, MISSING FEATURES OR MISTAKES

1. Er is geen check for checkmate, dus de game eindigt nooit.
2. Koning kan castlen terwijl er een stuk van het ander team, het pad aanvalt.
3. Pawns kunnen niet promoveren.
4. Ik gebruik te veel global variabels, hierdoor moet alles in een file zitten. Dit is heel erg onhandig en 
onoverzichtelijk.


EVALUATION CRITERIA

Pawn Weight +10 (Elke pawn is 10 punten waard) - done
Isolated pawns -1 per (Een pawn dat geïsoleerd is van andere pawns) - done
Doubled pawns -1 per (Twee pawns op de zelfde column) - done
Pawns in center +2 (Pawn zit tussen D4 en E5) - done
Pawn almost promoting +5 (Pawn op de rij 7 of rij 2) - done

Knight Weight +30 (Elke knight is 30 punten waard) - done
Knight in center +2 (Knight staat tussen D4 en E5) - done
Knight near center +1 (Knight staat tussen C4 en F6) - done
Knight on the rim -1 (Knight ligt aan de buitenste kant) - done

Bishop Weight +30 (Elke bishop is 30 punten waard) - done
Bishop on long diagonal +2 (Bishop zit op de langste diagonalen) - done
Bishop near center +1 (Bishop staat tussen C4 en F6) - done
Bishop on the rim -1 (Bishop ligt aan de buitenste kant) - done

Rook Weight +50 (Elke rook is 50 punten waard) - done
Rook on seventh rank +4 (Rook staat op rij 7) - done
Rook on openfile +3 (Rook staat op een column zonder pawns) - done
Rook behind past pawn +4 (Rook staat op dezelfde column achter een past pawn) - done

Queen Weight +90 (Elke queen is 90 punten waard) - done
Queen and knight exist +2 (Er is een queen en knight) - done

King Weight +300 (Elke king is 300 punten waard) - done
King castle right lost -4 (Koning heeft castle rights verloren) - done
King castle made +3 (Koning heeft gecasteld) - done
King distance from beginrow -1 per row (Koning krijgt minpunten per rij dat hij weg is van de beginrij) - done

"""

# ChessPiece en Square zijn grotendeels gemaakt door:
# https://stackoverflow.com/questions/50232639/drag-and-drop-qlabels-with-pyqt5


class Board():
    def __init__(self):
        self.allSquares
        self.whitePieces
        self.blackPieces
        self.currentWhitePieces
        self.currentBlackPieces
        self.turnCount = 0


class ChessPiece(QLabel):
    # Class voor alle schaakstukken
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.hasMoved = False
        self.board

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        # Doe dit als een chesspiece op een chesspiece valt.
        global turnCount

        if (turnCount % 2 == 0) and ("white" in clickedPieceObject.objectName()):

            # Hier checken we of een ChessPiece een andere ChessPiece mag aanvallen
            # Als de square in .getLegalMoves() zit, dan kunnen we hem aanvallen
            if (self.getPosition() in clickedPieceObject.getLegalMoves()):

                # We veranderen de positie van het object dat geclicked is.
                clickedPiecePreviousPosition = clickedPieceObject.pos()
                clickedPieceObject.move(self.pos())

                # Hier halen we het stuk dat wordt aangevallen weg. Ik heb meerdere manieren geprobeerd zoals gezegd op
                # websites zoals stackoverflow, maar het is mij niet gelukt. Daarom moet ik hem simpel weg verplaatsen
                # uit het scherm
                self.move(-100, -100)
                currentBlackPieces.remove(self)

                # Als de koning wordt aangevallen nadat de move wordt gedaan, dan is de move illegaal.
                # Dit is niet een goede manier om te checken wat de legal moves zijn van de koning, want dan kunnen we
                # niet checken voor checkmate. Maar ik wist niet hoe je moest checken wat de legal moves zijn als de
                # koning in check was.
                if len(whitePieces[-1].underAttack()) != 0:
                    self.move(clickedPieceObject.pos())
                    clickedPieceObject.move(clickedPiecePreviousPosition)
                    print("King would be under attack!")
                    currentBlackPieces.append(self)

                # Als de koning niet wordt aangevallen nadat de move wordt gedaan, dan gaan updaten we de evaluatie en
                # geven we de beurt aan de andere persoon.
                else:
                    clickedPieceObject.hasMoved = True
                    turnCount += 1
                    evaluationBar.evaluateBoard()
                    # Als de koning heeft bewogen, dan heeft hij de castleRights verloren.
                    if "king" in clickedPieceObject.objectName():
                        self.castleRights = False
                event.acceptProposedAction()

            else:
                # Als een chesspiece niet naar een square kan, dan betekent het dat hij daar niet naar toe kan gaan,
                # want die square zit niet in .getLegalMoves()
                print(clickedPieceObject.objectName() + " can't go to " + self.objectName())

        # Precies hetzelfde hier, behalve dan voor zwart.
        elif (turnCount % 2 == 1) and ("black" in clickedPieceObject.objectName()):

            if (self.getPosition() in clickedPieceObject.getLegalMoves()):
                clickedPiecePreviousPosition = clickedPieceObject.pos()
                clickedPieceObject.move(self.pos())
                self.move(-100, -100)
                currentWhitePieces.remove(self)

                if len(blackPieces[-1].underAttack()) != 0:
                    self.move(clickedPieceObject.pos())
                    clickedPieceObject.move(clickedPiecePreviousPosition)
                    print("King would be under attack!")
                    currentWhitePieces.append(self)
                else:
                    clickedPieceObject.hasMoved = True
                    turnCount += 1
                    evaluationBar.evaluateBoard()
                event.acceptProposedAction()

            else:
                print(clickedPieceObject.objectName() + " can't go to " + self.objectName())
        else:
            print("Het is niet jouw beurt!")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        # Dit gebeurt er als de muis beweegt.
        # Heel eerlijk gezegd begrijp ik niet zo goed wat hier gebeurt.

        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()

        # Zet het schaakstuk dat beweegt als clickedPieceObject.
        # Dit zullen we later gebruiken om te bepalen welke schaakstukken we moeten bewegen.
        global clickedPieceObject
        clickedPieceObject = self

        # Dit deel begrijp ik niet zo goed.
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
        global allSquares

        # Loop door alle squares om te kijken of de posities hetzelfde zijn.
        for square in allSquares:
            if self.pos() == square.pos():
                return square


class Square(QLabel):
    # Dit is de class voor alle squares. Bijvoorbeeld de square A1
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        # Dit gebeurt er als er iets wordt gedropt op een square.

        global turnCount

        # Check wiens beurt het is en welke kleur wordt bewogen.
        if (turnCount % 2 == 0) and ("white" in clickedPieceObject.objectName()):
            # We hebben hier twee if statements voor de castle. Dit komt omdat ik ook de rook moest bewegen wanneer de
            # koning wou castlen. Ik wist niet een betere manier om dit te doen.

            # Doe dit als castle long en witte koning
            if (("king" in clickedPieceObject.objectName()) and (allSquares[16] == self) and (clickedPieceObject.hasMoved is False)):
                clickedPieceObject.move(self.pos())
                clickedPieceObject.hasMoved = True
                whitePieces[8].move(allSquares[24].pos())
                event.acceptProposedAction()
                turnCount += 1
                clickedPieceObject.hasCastled = True
                evaluationBar.evaluateBoard()

            # Doe dit als castle short en witte koning
            elif (("king" in clickedPieceObject.objectName()) and (allSquares[48] == self) and (
                    clickedPieceObject.hasMoved is False)):
                clickedPieceObject.move(self.pos())
                clickedPieceObject.hasMoved = True
                whitePieces[9].move(allSquares[40].pos())
                event.acceptProposedAction()
                turnCount += 1
                clickedPieceObject.hasCastled = True
                evaluationBar.evaluateBoard()

            # Doe dit als de moves geen castle moves waren.
            # Check hier ook of de square in legalMoves zit.
            elif (self in clickedPieceObject.getLegalMoves()):

                clickedPiecePreviousPosition = clickedPieceObject.pos()
                clickedPieceObject.move(self.pos())
                clickedPieceObject.hasMoved = True

                # Dit is hetzelfde als bij Chesspiece met dezelfde redenen en dezelfde flaws.
                if len(whitePieces[-1].underAttack()) != 0:
                    clickedPieceObject.move(clickedPiecePreviousPosition)
                    print("King would be under attack!")
                else:
                    clickedPieceObject.hasMoved = True
                    turnCount += 1
                    if "king" in clickedPieceObject.objectName():
                        clickedPieceObject.castleRights = False
                    evaluationBar.evaluateBoard()
                event.acceptProposedAction()
            else:
                print(clickedPieceObject.objectName() + " can't go to " + self.objectName())

        # Dit is precies hetzelfde, maar dan met zwart.
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
                clickedPieceObject.hasCastled = True
                evaluationBar.evaluateBoard()

            # Doe dit als castle short en zwarte koning
            elif (("king" in clickedPieceObject.objectName()) and (allSquares[55] == self) and (
                    clickedPieceObject.hasMoved is False)):
                clickedPieceObject.move(self.pos())
                clickedPieceObject.hasMoved = True
                blackPieces[9].move(allSquares[47].pos())
                event.acceptProposedAction()
                turnCount += 1
                clickedPieceObject.hasCastled = True
                evaluationBar.evaluateBoard()

            elif (self in clickedPieceObject.getLegalMoves()):
                clickedPiecePreviousPosition = clickedPieceObject.pos()
                clickedPieceObject.move(self.pos())
                event.acceptProposedAction()

                if len(blackPieces[-1].underAttack()) != 0:
                    clickedPieceObject.move(clickedPiecePreviousPosition)
                    print("King would be under attack!")
                else:
                    clickedPieceObject.hasMoved = True
                    turnCount += 1
                    if "king" in clickedPieceObject.objectName():
                        clickedPieceObject.castleRights = False
                    evaluationBar.evaluateBoard()

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


class Knight(ChessPiece):
    # De knight heeft een unieke patroon. Hij kan twee squares naar voren en dan naar links of rechts gaan.
    # Het maakt niet uit voor de knight of er iets staat op zijn pad.

    def getLegalMoves(self):
        # NOTE = Er is een veel efficientere manier om dit te doen. Helaas kwam ik hier later pas achter, dus voorlopig
        # laat ik het staan. Als ik nog tijd heb later, dan verbeter ik dit. (Het kan echt VEEL efficienter, alles is nu
        # brute force)

        # Return een lijst met squares die kunnen worden aangevallen door een knight
        possibleAttackSquares = []

        # Loop door alle squares die links van de knight zijn.
        for square in self.getAttackSquaresLeftSide():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                # Als er een stuk staat op die plek, dan moeten we kijken of het een witte stuk is of een zwarte stuk
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    # Als het van een andere team is, dan voegen we hem toe aan de mogelijke squares die we kunnen
                    # aanvallen.
                    possibleAttackSquares.append(square)

        # Loop door alle squares die boven de knight zijn.
        for square in self.getAttackSquaresAbove():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)

        # Loop door alle squares die rechts van de knight zijn.
        for square in self.getAttackSquaresRightSide():
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                if square.containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    possibleAttackSquares.append(square)

        # Loop door alle squares die onder de knight zijn.
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

        # Dit zijn de twee squares waar we naar zoeken
        searchSquares = [alphabet[alphabet.find(column) - 2] + str(int(row) - 1),
                         alphabet[alphabet.find(column) - 2] + str(int(row) + 1)]

        # Brute force zoek door alle squares heen.
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

    def getValue(self):
        # Return de waarde van een knight gebaseerd op de locatie van de knight en de waarde van de knight.
        knightWeight = 30

        # De knight kan het meest doen wanneer hij in het midden zit. Hier kan hij veel squares aanvallen.

        # Als de positie van de knight tussen D4 en E5 zitten, krijgen ze extra punten.
        if ("D" <= self.getPosition().objectName()[-2] <= "E") and (4 <= int(self.getPosition().objectName()[-1]) <= 5):
            knightPositionWeight = 2

        # Als de positie van de knight tussen C3 en F6 zitten, krijgen ze minder extra punten.
        elif ("C" <= self.getPosition().objectName()[-2] <= "F") and (3 <= int(self.getPosition().objectName()[-1]) <= 6):
            knightPositionWeight = 1

        # Als de positie van de knight aan de buitenste kant ligt, dan krijgen ze min punten.
        elif (self.getPosition().objectName()[-2] == "A" or "H") or (int(self.getPosition().objectName()[-1]) == 1 or 8):
            knightPositionWeight = -1

        # Op alle andere plekken de waarde van de knight 0
        else:
            knightPositionWeight = 0
        return knightWeight + knightPositionWeight


class Bishop(ChessPiece):
    # De bishop kan diagonaal aanvallen.
    def getLegalMoves2(self):
        attackAbleSquares = []
        beginSquareIndex = 0

        for square in allSquares:
            if self.getPosition() == square:
                break
            else:
                beginSquareIndex += 1

        index = 0

        while 8 > int(allSquares[beginSquareIndex + index * 9].objectName()[-1]) > 1 and \
            "H" > allSquares[beginSquareIndex + index * 9].objectName()[-2] > "A":

            index += 1
            if allSquares[beginSquareIndex + index * 9].containsPiece() is None:
                attackAbleSquares.append(allSquares[beginSquareIndex + index * 9].objectName())
            else:
                if allSquares[beginSquareIndex + index * 9].containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    attackAbleSquares.append(allSquares[beginSquareIndex + index * 9].objectName())
                    break
                else:
                    break

        return attackAbleSquares

    def getLegalMoves(self):
        # NOTE: Ook hier kan het veel efficienter.
        # Return een lijst met squares die kunnen worden aangevallen door een bishop
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

    def getAttackSquaresDiagNEBetter(self):
        # Ik moet hier nog meer aan werken. Dit zal een betere versie zijn dan de vorige met minder lines.
        # Haalt alle squares die NE (north east) van het ChessPiece kunnen worden aangevallen.
        attackAbleSquares = []
        beginSquareIndex = 0

        # Vind de index van de beginsquare.
        for square in allSquares:
            if self.getPosition() == square:
                break
            else:
                beginSquareIndex += 1

        # Zoek hier de square die rechts boven
        index = 0
        while 8 > int(allSquares[beginSquareIndex + index * 9].objectName()[-1]) > 1 and \
            "H" > allSquares[beginSquareIndex + index * 9].objectName()[-2] > "A":

            index += 1
            if allSquares[beginSquareIndex + index * 9].containsPiece() is None:
                attackAbleSquares.append(allSquares[beginSquareIndex + index * 9].objectName())
            else:
                if allSquares[beginSquareIndex + index * 9].containsPiece().objectName()[0:5] != self.objectName()[0:5]:
                    attackAbleSquares.append(allSquares[beginSquareIndex + index * 9].objectName())
                    break
                else:
                    break

        return attackAbleSquares

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
        except IndexError:
            pass

        for square in allSquares:
            for search in temp:
                if search in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def bishopLongdiagonal(self):
        # Returnt een boolean dat bepaalt of de bishop op de long diagonal zit of niet.

        # Dit is de diagonaal van links beneden naar rechts boven.
        for i in range(8):
            # Als de positie van de bishop hierop ligt, dan geven we hem extra punten.
            if self.pos() == allSquares[0 + i * 9]:
                return True
        # Dit is de diagonaal van links boven naar rechts beneden.
        for i in range(8):
            if self.pos() == allSquares[7 + i * 7]:
                return True
        # Als ze er niet op zitten, dan return false.
        return False

    # De bishop is sterk wanneer je hem fianchetto. Als hij op de "long diagonal" zit, dan geven we hem extra punten.
    # Verder is de bishop ook erg actief als hij in het midden zit. Als hij aan de buitenkant ligt, dan geven we hem
    # minpunten.
    def getValue(self):
        bishopWeight = 30

        # Als de bishop op de long diagonal zit, geef ze extra punten.
        if self.bishopLongdiagonal() is True:
            bishopPositionWeight = 2

        # Als de bishop tussen C3 en F6 zitten, geven ze minder extra punten
        elif ("C" <= self.getPosition().objectName()[-2] <= "F") and (3 <= int(self.getPosition().objectName()[-1]) <= 6):
            bishopPositionWeight = 1

        # Als de positie van de bishop aan de buitenste kant ligt, dan krijgen ze min punten.
        elif (self.getPosition().objectName()[-2] == "A" or "H") or (
                    int(self.getPosition().objectName()[-1]) == 1 or 8):
            bishopPositionWeight = -1

        # Ze krijgen geen punten als ze op andere plekken zijn
        else:
            bishopPositionWeight = 0

        return bishopWeight + bishopPositionWeight


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
        for square in allSquares:
            if (column == square.objectName()[-2] and int(row) > int(square.objectName()[-1])):
                possibleAttackSquares.insert(0, square)
        return possibleAttackSquares

    def getAttackSquaresAbove(self):
        # Return een lijst met alle squares die boven het schaakstuk zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2]
        possibleAttackSquares = []
        for square in allSquares:
            if (column == square.objectName()[-2] and int(row) < int(square.objectName()[-1])):
                possibleAttackSquares.append(square)
        return possibleAttackSquares

    def getAttackSquaresRight(self):
        # Return een lijst met alle squares die rechts van het schaakstuk zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2]
        possibleAttackSquares = []
        for square in allSquares:
            if (column < square.objectName()[-2] and row == square.objectName()[-1]):
                possibleAttackSquares.append(square)
        return possibleAttackSquares

    def getAttackSquaresLeft(self):
        # Return een lijst met alle squares die links van het schaakstuk zitten.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2]
        possibleAttackSquares = []
        for square in allSquares:
            if (column > square.objectName()[-2] and row == square.objectName()[-1]):
                possibleAttackSquares.insert(0, square)
        return possibleAttackSquares

    def openFile(self):
        # Return een boolean gebaseerd op of de rook op een openFile is of niet.
        # Een open file is een column zonder pawns.
        column = self.getPosition().objectName()[-2]
        # Loop door alle squares
        for square in allSquares:
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
            for square in allSquares:
                # Zoek naar de square met dezelfde column en de rij 7
                if square.objectName()[-2] == currentColumn and square.objectName()[-1] == "7" and square.containsPiece() is not None:
                    if "white_pawn" in square.containsPiece().objectName() and int(self.getPosition().objectName()[-1]) < 7:
                        return True
                    else:
                        break

        elif "black" in self.objectName():
            for square in allSquares:
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

        # Als de rook op de 7de rij staat, dan krijgt hij extra punten
        if self.getPosition().objectName()[-2] == "7":
            rookPositionWeight += 4

        # Als de rook op een open file staat, dan krijgt hij +3 punten
        elif self.openFile() is True:
            rookPositionWeight += 3

        elif self.protectingPastPawn() is True:
            rookPositionWeight += 5

        return rookWeight + rookPositionWeight


class Queen(Rook, Bishop):
    def getLegalMoves(self):
        possibleAttackSquares = []

        # De queen kan bewegen net als een rook en een biship. Daarom gebruiken we hun methodes.

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
            for piece in currentWhitePieces:
                if "knight" in piece.objectName():
                    queenPositionWeight += 2
        elif "black" in self.objectName():
            for piece in currentBlackPieces:
                if "knight" in piece.objectName():
                    queenPositionWeight += 2

        return queenWeight + queenPositionWeight


class King(ChessPiece):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.hasMoved = False
        self.castleRights = True
        self.hasCastled = False

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
                    for piece in currentBlackPieces[:-1]:
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
                    for piece in currentWhitePieces[:-1]:
                        if square in piece.getLegalMoves():
                            attackingPieces.append(piece)
                            break
                        elif "pawn" in piece.objectName():
                            if square in piece.getAttackSquaresDiagonally():
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

        for square in allSquares:
            for name in squareNames:
                if name in square.objectName():
                    possibleAttackSquares.append(square)

        return possibleAttackSquares

    def castleLong(self):
        # Return een square, als castleLong een legal move is.

        # De koning mag niet hebben bewogen voor de castle
        if self.hasMoved is False:
            # Condities voor een long castle:
            # 1. A1 is NIET leeg, 2. A1.hasMoved is False, B1 is leeg, 3. C1 is leeg, 4. D1 is leeg, en koning is wit.
            if allSquares[0].containsPiece() is not None:
                if ("white" in self.objectName()) and (allSquares[0].containsPiece().hasMoved is False) and \
                        (allSquares[8].containsPiece() is None) and (allSquares[16].containsPiece() is None) \
                        and (allSquares[24].containsPiece() is None):
                    return allSquares[16]

            # Precies dezelfde condities maar nu is het de 8ste rij. Dus B8, C8, D8 en koning is zwart.
            elif allSquares[7].containsPiece() is not None:
                if ("black" in self.objectName()) and (allSquares[7].containsPiece().hasMoved is False) and \
                        (allSquares[15].containsPiece() is None) and (allSquares[23].containsPiece() is None) \
                        and (allSquares[31].containsPiece() is None):
                    return allSquares[23]

    # Check of castleshort available is
    def castleShort(self):
        # Return een square, als castle short een legal move is.
        # De koning mag niet hebben bewogen voor de castle.
        if self.castleRights is True:
            # Condities voor een short castle:
            # 1. H1 is NIET leeg, 2. H1.hasMoved is False, G1 is leeg, 3. F1 is leeg en koning is wit.
            if allSquares[56].containsPiece() is not None:
                if ("white" in self.objectName()) and (allSquares[56].containsPiece().hasMoved is False) and \
                        (allSquares[48].containsPiece() is None) and (allSquares[40].containsPiece() is None):
                    return allSquares[48]

            # Precies dezelfde condities maar nu is het de 8ste rij. Dus H8, G8 en F1 en de koning is zwart.
            elif allSquares[63].containsPiece() is not None:
                if ("black" in self.objectName()) and (allSquares[63].containsPiece().hasMoved is False) and \
                        (allSquares[55].containsPiece() is None) and (allSquares[47].containsPiece() is None):
                    return allSquares[55]

    # Check of de koning wordt aangevallen en return de piece(s) dat de koning aanvalt.
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


class WhitePawn(ChessPiece):
    # Een white pawn kan naar boven gaan en valt de twee squares aan die diagonaal boven de pawn staan.
    def getLegalMoves(self):
        possibleAttackSquares = []

        # Loop door alle squares boven de pawn
        for square in self.getAttackSquaresAbove():
            # Als er niks voor hem staat kan de pawn vooruit
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                break

        # Loop door de twee squares die diagonaal van de pawn zijn.
        for square in self.getAttackSquaresDiagonally():
            # Als er iets op de squares zitten, dan kan de pawn hem aanvallen
            if square.containsPiece() != None and "black" in square.containsPiece().objectName():
                possibleAttackSquares.append(square)

        return possibleAttackSquares

    def getAttackSquaresDiagonally(self):
        # Return een lijst van squares die kunnen worden aangevallen. De squares zijn diagonaal van de pawn. De squares
        # kunnen alleen twee squares zijn die diagonaal van hem staan.
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
        # Return squares die boven de pawn zitten waar de pawn naar toe zou kunnen.
        currentSquare = self.getPosition().objectName()
        row = currentSquare[-1:]
        column = currentSquare[-2: -1]
        possibleAttackSquares = []

        # Als de pawn nog niet beweegt heeft, dan mag hij 2 squares omhoog.
        if self.hasMoved == False:
            for square in allSquares:
                if ((column == square.objectName()[-2] and int(row) + 1 == int(square.objectName()[-1])) or
                        (column == square.objectName()[-2] and int(row) + 2 == int(square.objectName()[-1]))):
                    possibleAttackSquares.append(square)
        else:
            # Anders mag hij alleen 1 square omhoog
            for square in allSquares:
                if column == square.objectName()[-2] and int(row) + 1 == int(square.objectName()[-1]):
                    possibleAttackSquares.append(square)
        return possibleAttackSquares

    def checkIsolatedPawns(self):
        # Returnt een boolean dat bepaalt of de pawn geisoleerd is of niet.
        # Geisoleerde pawns zijn pawns die geen pawns naast hun hebben.

        # Maak een lijst met huidige pawns
        currentPawns = []
        for piece in currentWhitePieces:
            if "pawn" in piece.objectName():
                currentPawns.append(piece)

        # Zet de huidige naam van de column van de pawn als currentColumn
        currentColumn = self.getPosition().objectName()[-2]

        # Zoek door alle pawns heen. Als ze naast de pawn zitten, dan is hij niet geisoleerd.
        for pawn in currentPawns:
            # Als er een pawn naast de pawn staat, dan is hij niet geisoleerd
            if pawn.getPosition().objectName()[-2] == string.ascii_uppercase[string.ascii_uppercase.find(currentColumn) - 1]\
                    or pawn.getPosition().objectName()[-2] == string.ascii_uppercase[string.ascii_uppercase.find(currentColumn) + 1]:
                return False
        # Als ze door de hele loop zijn gegaan en ze kunnen geen pawn vinden dat naast hun staat, dan is hij geisoleerd
        return True

    def checkDoubledPawns(self):
        # Returnt een boolean gebaseerd op of de pawn een deel is van een paar doubled pawns.
        # Een doubled pawn zijn twee pawns op dezelfde column.

        # Maak een lijst met huidige pawns
        currentPawns = []
        for piece in currentWhitePieces:
            if "pawn" in piece.objectName():
                currentPawns.append(piece)

        # Zet de huidige naam van de column van de pawn als currentColumn
        currentColumn = self.getPosition().objectName()[-2]

        # Loop door alle pawns
        for pawn in currentPawns:
            # Als de pawn op dezelfde column zit als een andere pawn, dan is hij doubled.
            if pawn.getPosition().objectName()[-2] == currentColumn and self != pawn:
                return True
        return False

    def getValue(self):
        whitePawnWeight = 10

        # Als de pawn tussen D4 en E5 zit, dan krijgt hij extra punten
        if ("D" <= self.getPosition().objectName()[-2] <= "E") and (4 <= int(self.getPosition().objectName()[-1]) <= 5):
            pawnPositionWeight = 2
        # Als de pawn bijna promoveert krijgt hij ook extra punten.
        elif "7" == self.getPosition().objectName()[-1]:
            pawnPositionWeight = 5

        # Op elke andere plek krijgen ze geen extra punten.
        else:
            pawnPositionWeight = 0

        # Als de pawn geisoleerd is dan krijgt hij -1 punt.
        if self.checkIsolatedPawns() is True:
            pawnPositionWeight -= 1

        # Als de pawn doubled is dan krijgt hij -1 punt.
        if self.checkDoubledPawns() is True:
            pawnPositionWeight -= 1

        return whitePawnWeight + pawnPositionWeight


class BlackPawn(ChessPiece):
    # Een black pawn kan naar beneden gaan en valt de twee squares aan die diagonaal onder de pawn staan.
    def getLegalMoves(self):
        possibleAttackSquares = []

        # Loop door alle squares boven de pawn.
        for square in self.getAttackSquaresAbove():
            # Als er niks voor hem staat kan de pawn vooruit
            if square.containsPiece() == None:
                possibleAttackSquares.append(square)
            else:
                break

        # Loop door de twee squares die diagonaal van de pawn zijn.
        for square in self.getAttackSquaresDiagonally():
            # Als er iets diagonaal van de pawn staat, dan kan de pawn hem aanvallen
            if square.containsPiece() != None and "white" in square.containsPiece().objectName():
                possibleAttackSquares.append(square)

        return possibleAttackSquares


    def getAttackSquaresDiagonally(self):
        # Return een lijst van squares die kunnen worden aangevallen. De squares zijn diagonaal van de pawn. De squares
        # kunnen alleen twee squares zijn die diagonaal van hem staan.
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
        # Return de squares boven de pawn, waar de pawn naar toe kan.
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

    def checkIsolatedPawns(self):
        # Returnt een boolean dat bepaalt of de pawn geisoleerd is of niet.

        # Maak een lijst met huidige pawns
        currentPawns = []
        for piece in currentBlackPieces:
            if "pawn" in piece.objectName():
                currentPawns.append(piece)

        # Zet de huidige naam van de column van de pawn als currentColumn
        currentColumn = self.getPosition().objectName()[-2]

        # Zoek door alle pawns heen. Als ze naast de pawn zitten, dan is hij niet geisoleerd.
        for pawn in currentPawns:
            # Als er een pawn is dat naast hun staat, is hij niet geisoleerd
            if pawn.getPosition().objectName()[-2] == string.ascii_uppercase[string.ascii_uppercase.find(currentColumn) - 1]\
                    or pawn.getPosition().objectName()[-2] == string.ascii_uppercase[string.ascii_uppercase.find(currentColumn) + 1]:
                return False
        # Als ze door de hele loop zijn gegaan en ze kunnen geen pawn vinden dat naast hun staat, dan is hij geisoleerd
        return True

    def checkDoubledPawns(self):
        # Returnt een boolean als de pawn een deel is van een doubled pawns.
        # Een doubled pawn zijn twee pawns op dezelfde column.

        # Maak een lijst met huidige pawns
        currentPawns = []
        for piece in currentBlackPieces:
            if "pawn" in piece.objectName():
                currentPawns.append(piece)

        # Zet de huidige naam van de column van de pawn als currentColumn
        currentColumn = self.getPosition().objectName()[-2]

        # Loop door alle pawns
        for pawn in currentPawns:
            # Als de pawn op dezelfde column zit als een andere pawn, dan is hij doubled.
            if pawn.getPosition().objectName()[-2] == currentColumn and self != pawn:
                return True
        return False

    def getValue(self):
        blackPawnWeight = 10

        # Als de pawn tussen D4 en E5 zit, dan krijgt hij extra punten
        if ("D" <= self.getPosition().objectName()[-2] <= "E") and (4 <= int(self.getPosition().objectName()[-1]) <= 5):
            pawnPositionWeight = 2

        # Als de pawn bijna promoveert krijgt hij ook extra punten.
        elif "2" == self.getPosition().objectName()[-1]:
            pawnPositionWeight = 5

        # Op elke andere plek krijgen ze geen extra punten.
        else:
            pawnPositionWeight = 0

        # Als de pawn geisoleerd is dan krijgt hij -1 punt.
        if self.checkIsolatedPawns() is True:
            pawnPositionWeight -= 1

        # Als de pawn doubled is dan krijgt hij -1 punt.
        if self.checkDoubledPawns() is True:
            pawnPositionWeight -= 1

        return blackPawnWeight + pawnPositionWeight


class Evaluate(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)

    # Return de value van alle witte stukken
    def whitePieceValue(self):
        totalValue = 0
        for piece in currentWhitePieces:
            totalValue += piece.getValue()
        return totalValue

    # Return de value van alle zwarte stukken
    def blackPieceValue(self):
        totalValue = 0
        for piece in currentBlackPieces:
            totalValue += piece.getValue()
        return totalValue

    # Verander de text van de evaluation label in de huidige evaluation.
    def evaluateBoard(self):
        self.setText("Evaluation: " + str(round((self.whitePieceValue() - self.blackPieceValue()) * 0.1, 2)))


from PyQt5 import QtCore, QtGui, QtWidgets

# Bijna alles in UI_MAINWINDOW is gemaakt met de tool "Qt Designer"
# Ik heb alleen de klassen verandert van de schaakstukken en variabelen toegevoegd aan het einde.
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 840)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.evaluationbar = Evaluate(self.centralwidget)
        self.evaluationbar.setGeometry(QtCore.QRect(350, 800, 100, 20))
        self.evaluationbar.setText("Evaluation: ")
        self.evaluationbar.setObjectName("evaluationBar")
        self.evaluationbar.setStyleSheet("border: 1px solid black;")
        self.evaluationbar.raise_()
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
        global evaluationBar

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

        evaluationBar = self.evaluationbar

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())