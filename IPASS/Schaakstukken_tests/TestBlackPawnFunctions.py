import unittest
import sys

from PyQt5 import QtWidgets

from myRepository.IPASS.Chess import Ui_MainWindow


class TestBlackPawnFunctions(unittest.TestCase):

    def testGetLegalMoves(self):
        # Test de getLegalMoves functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin kan de zwarte pawn op de A column 2 stappen naar voren, naar de squares A6 en A5.
        actual = []
        for square in ui.black_pawn_a.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(['squareA6', 'squareA5'], actual)

        # Daarna kan de zwarte pawn alleen 1x naar voren.
        ui.black_pawn_a.move(0, 200)
        ui.black_pawn_a.hasMoved = True
        actual = []
        for square in ui.black_pawn_a.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(['squareA5'], actual)

        # Als er iets diagonaal van de pawn staat en het is van het andere team, dan kan de pawn hem aanvallen.
        ui.white_pawn_a.move(100, 300)
        actual = []
        for square in ui.black_pawn_a.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(['squareA5', 'squareB5'], actual)

    def testCheckIsolatedPawns(self):
        # Test de checkIsolated functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin is geen een pawn geisoleerd
        self.assertEqual(False, ui.black_pawn_a.checkIsolated())

        # Als de pawn op de column B weg gaat, dan hoort de pawn op de column A geisoleerd te zijn.
        ui.black_pawn_b.move(0, 200)
        self.assertEqual(True, ui.black_pawn_a.checkIsolated())

    def testCheckDoubledPawns(self):
        # Test de checkDoubledPawns functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin is geen een pawn doubled
        self.assertEqual(False, ui.black_pawn_a.checkDoubledPawns())

        # Maar als we de pawn op column B verzetten naar dezelfde column als pawn A, dan is hij doubled.
        ui.black_pawn_b.move(0, 200)
        self.assertEqual(True, ui.black_pawn_a.checkDoubledPawns())

    def testGetValue(self):
        # Test de getValue functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin hoort de value 10 te zijn.
        self.assertEqual(10, ui.black_pawn_d.getValue())

        # Als de pawn in het midden is, dan krijgt hij extra punten
        ui.black_pawn_d.move(300, 400)
        self.assertEqual(12, ui.black_pawn_d.getValue())

        # Als de pawn op de pawn bijna promoveert, krijgt hij extra punten
        ui.black_pawn_d.move(300, 600)
        self.assertEqual(15, ui.black_pawn_d.getValue())
