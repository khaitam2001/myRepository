import unittest
import sys

from PyQt5 import QtWidgets

from myRepository.IPASS.Chess import Ui_MainWindow


class TestKnightFunctions(unittest.TestCase):

    def testGetLegalMoves(self):
        # Test de getLegalMoves functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin kan de knight op B2 alleen naar A3 en C3.
        actual = []
        for square in ui.white_knight_b.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(['squareA3', 'squareC3'], actual)

        # Als we hem op D4 zetten, dan kan de knight naar 6 plekken toe.
        ui.white_knight_b.move(300, 400)
        actual = []
        for square in ui.white_knight_b.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(['squareB3', 'squareB5', 'squareC6', 'squareE6', 'squareF3', 'squareF5'], actual)

    def testGetValue(self):
        # Test de getValue functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin is de knight aan de zijkant en dus verliest hij 1 punt van zijn 30 punten.
        self.assertEqual(29, ui.white_knight_b.getValue())

        # Maar als we hem in het midden zetten, krijgt hij 2 extra punten.
        ui.white_knight_b.move(400, 400)
        self.assertEqual(32, ui.white_knight_b.getValue())

        # Als hij net buiten het midden zit, krijgt hij 1 extra punt.
        ui.white_knight_b.move(500, 500)
        self.assertEqual(31, ui.white_knight_b.getValue())
