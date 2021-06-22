import unittest
import sys

from PyQt5 import QtWidgets

from myRepository.IPASS.Chess import Ui_MainWindow


class TestRookFunctions(unittest.TestCase):

    def testGetLegalMoves(self):
        # Test de getLegalMoves functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin kan de rook nergens naartoe
        self.assertEqual([], ui.white_rook_a.getLegalMoves())

        # Als de pawn weg zou zijn, dan kan de rook naar alles boven hem, totdat hij een andere chesspiece ontmoet.
        ui.white_pawn_a.move(-100, -100)
        actual = []
        for square in ui.white_rook_a.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(['squareA2', 'squareA3', 'squareA4', 'squareA5', 'squareA6', 'squareA7'], actual)

        # Als hij op E4 staat in het begin, dan kan hij naar 11 squares toe.
        ui.white_rook_a.move(400, 400)
        actual = []
        for square in ui.white_rook_a.getLegalMoves():
            actual.append(square.objectName())
        self.assertEqual(['squareE3', 'squareE5', 'squareE6', 'squareE7', 'squareD4', 'squareC4',
                          'squareB4', 'squareA4', 'squareF4', 'squareG4', 'squareH4'], actual)

    def testOpenFile(self):
        # Test de openFile functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin is de rook niet op een open file.
        self.assertEqual(False, ui.white_rook_a.openFile())

        # Als de twee pawns op de column A weg zijn, dan is hij op een openfile.
        ui.white_pawn_a.move(-100, -100)
        ui.black_pawn_a.move(-100, -100)
        self.assertEqual(True, ui.white_rook_a.openFile())

    def testProtectingPastPawn(self):
        # Test de protectingPastPawn functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In de volgende scenario is de witte pawn op rij 7 en zit een rook hem te beschermen.
        ui.black_pawn_a.move(-100, -100)
        ui.white_pawn_a.move(0, 100)
        self.assertEqual(True, ui.white_rook_a.protectingPastPawn())

        # In de volgende scenario is de zwarte pawn op rij 2 en zit een rook hem te beschermen.
        ui.black_pawn_a.move(0, 600)
        ui.white_pawn_a.move(-100, -100)
        self.assertEqual(True, ui.black_rook_a.protectingPastPawn())

    def testGetValue(self):
        # Test de getValue functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin is hij 50 punten waard
        self.assertEqual(50, ui.white_rook_a.getValue())

        # Als een witte rook op de 7de rij staat, krijgt hij 4 extra punten
        ui.black_pawn_a.move(-100, -100)
        ui.white_rook_a.move(0, 100)
        self.assertEqual(54, ui.white_rook_a.getValue())

