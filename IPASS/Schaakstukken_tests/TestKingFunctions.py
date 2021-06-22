import unittest
import sys

from PyQt5 import QtWidgets

from myRepository.IPASS.Chess import Ui_MainWindow


class TestKingFunctions(unittest.TestCase):

    def testGetLegalMoves(self):
        # Test de getLegalMoves functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin kan de koning nergens naartoe
        self.assertEqual([], ui.black_king.getLegalMoves())

        # Als de plek voor koning vrij is, dan kan de koning er naartoe
        ui.black_pawn_e.move(-100, -100)
        actual = []
        for square in ui.black_king.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(["squareE7"], actual)

        # Als die zelfde plek bezet is door een vijand, dan kan de koning hem aanvallen.
        ui.white_bishop_c.move(400, 100)
        actual = []
        for square in ui.black_king.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(["squareE7"], actual)

    def testCastleLong(self):
        # Test de castleLong functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin kan de koning niet castlen
        self.assertEqual(None, ui.black_king.castleLong())

        # Als de plekken vrij zijn, dan kan de koning wel castlen
        ui.white_bishop_c.move(-100, -100)
        ui.white_knight_b.move(-100, -100)
        ui.white_queen.move(-100, -100)
        self.assertEqual("squareC1", ui.white_king.castleLong().objectName())

        # Maar als de koning geen castleRights heeft dan kan hij niet castlen
        ui.white_king.castleRights = False
        self.assertEqual(None, ui.white_king.castleLong())

    def testCastleShort(self):
        # Test de castleShort functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin kan de koning niet castlen
        self.assertEqual(None, ui.white_king.castleShort())

        # Als de plekken vrij zijn, dan kan de koning wel castlen
        ui.white_bishop_f.move(-100, -100)
        ui.white_knight_g.move(-100, -100)
        self.assertEqual("squareG1", ui.white_king.castleShort().objectName())

        # Maar als de koning geen castleRights heeft dan kan hij niet castlen
        ui.white_king.castleRights = False
        self.assertEqual(None, ui.white_king.castleShort())

    def testUnderAttack(self):
        # Test de testUnderAttack functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # Als de koning wordt aangevallen, dan geeft hij correct aan wie hem aanvalt.
        ui.black_queen.move(400, 400)
        ui.white_pawn_e.move(-100, -100)
        actual = []
        for piece in ui.white_king.underAttack():
            actual.append(piece.objectName())
        self.assertEqual(['black_queen'], actual)

        # Dit kunnen meerdere schaakstukken zijn.
        ui.white_pawn_d.move(-100, -100)
        ui.black_bishop_c.move(100, 400)
        actual = []
        for piece in ui.white_king.underAttack():
            actual.append(piece.objectName())
        self.assertEqual(['black_bishop_c', 'black_queen'], actual)

    def testGetValue(self):
        # Test de getValue functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin is de koning 903 punten waard, meer dan alle andere schaakstukken bij elkaar.
        self.assertEqual(903, ui.white_king.getValue())

        # Als de koning heeft gecastled, dan krijgt de koning 3 punten
        ui.white_king.hasCastled = True
        self.assertEqual(906, ui.white_king.getValue())

        # Als de koning niet meer kan castlen en nog niet heeft gecastled, dan verliest hij 4 punten.
        ui.white_king.hasCastled = False
        ui.white_king.castleRights = False
        self.assertEqual(899, ui.white_king.getValue())

    def testCheckForCheckmate(self):
        # Test de checkForCheckmate functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In de volgende scenario is de zwarte koning schaakmat dus hoort de functie true te geven
        ui.black_pawn_f.move(-100, -100)
        ui.board.currentBlackPieces.remove(ui.black_pawn_f)
        ui.white_queen.move(500, 100)
        ui.white_bishop_c.move(200, 400)
        self.assertEqual(True, ui.black_king.checkForCheckmate())

        # Maar als we een plek vrij maken voor de koning, waar de koning naar toe kan gaan, dan is het geen schaakmat
        ui.black_queen.move(-100, -100)
        ui.board.currentBlackPieces.remove(ui.black_queen)
        self.assertEqual(False, ui.black_king.checkForCheckmate())