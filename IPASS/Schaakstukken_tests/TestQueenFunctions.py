import unittest
import sys

from PyQt5 import QtWidgets

from myRepository.IPASS.Chess import Ui_MainWindow


class TestQueenFunctions(unittest.TestCase):

    def testGetLegalMoves(self):
        # Test de getLegalMoves functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # Als de queen in het begin op de square E4 staat, dan kan hij naar 19 verschillende squares.
        ui.white_queen.move(400, 400)
        self.assertEqual(19, len(ui.white_queen.getLegalMoves()))

    def testGetValue(self):
        # Test de getValue functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin is de queen 92 punten waard, want er bestaat een queen en een knight.
        self.assertEqual(92, ui.white_queen.getValue())

        # Als er geen knights zijn, dan krijgt de queen geen extra punten en dus is ze 90 punten waard
        ui.board.currentWhitePieces.remove(ui.white_knight_b)
        ui.board.currentWhitePieces.remove(ui.white_knight_g)
        self.assertEqual(90, ui.white_queen.getValue())