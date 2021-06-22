import unittest
import sys

from PyQt5 import QtWidgets

from myRepository.IPASS.Chess import Ui_MainWindow


class TestWhitePawnFunctions(unittest.TestCase):

    def testGetLegalMoves(self):
        # Test de getLegalMoves functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin kan de pawn 2 stappen naar voren.
        actual = []
        for square in ui.white_pawn_a.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(['squareA3', 'squareA4'], actual)

        # Als de pawn heeft bewogen kan hij alleen 1 stap naar voren.
        ui.white_pawn_a.hasMoved = True
        ui.white_pawn_a.move(0, 400)
        actual = []
        for square in ui.white_pawn_a.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(['squareA5'], actual)

        # Als er iets diagonaal van de pawn staat, dan kan hij dat aanvallen.
        ui.black_pawn_a.move(100, 300)
        actual = []
        for square in ui.white_pawn_a.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(['squareA5', 'squareB5'], actual)

        # Maar hij kan het niet aanvallen als het van zijn eigen team is.
        ui.black_pawn_a.move(-100, -100)
        ui.white_pawn_b.move(100, 300)
        actual = []
        for square in ui.white_pawn_a.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(['squareA5'], actual)

    def testCheckIsolatedPawns(self):
        # Test de checkIsolated functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin is de pawn niet geisoleerd.
        self.assertEqual(False, ui.white_pawn_a.checkIsolated())

        # Als we de pawn op de column B weghalen, dan is de pawn op column A geisoleerd.
        ui.board.currentWhitePieces.remove(ui.white_pawn_b)
        self.assertEqual(True, ui.white_pawn_a.checkIsolated())

    def testCheckDoubledPawns(self):
        # Test de checkDoubledPawns functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin is de pawn niet doubled.
        self.assertEqual(False, ui.white_pawn_a.checkDoubledPawns())

        # Als de pawn op column B verzetten naar column A, dan is er sprake van doubled pawns.
        ui.white_pawn_b.move(0, 500)
        self.assertEqual(True, ui.white_pawn_a.checkDoubledPawns())

    def testGetValue(self):
        # Test de getValue functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin krijgt de pawn geen extra punten.
        self.assertEqual(10, ui.white_pawn_a.getValue())

        # Als we de pawn in het midden krijgen, dan krijgt hij 2 extra punten.
        ui.white_pawn_d.move(300, 400)
        self.assertEqual(12, ui.white_pawn_d.getValue())

        # Als de pawn bijna promoveert, krijgt hij 5 extra punten.
        ui.white_pawn_d.move(300, 100)
        self.assertEqual(15, ui.white_pawn_d.getValue())