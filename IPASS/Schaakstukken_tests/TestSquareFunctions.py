import unittest
import sys

from PyQt5 import QtWidgets

from myRepository.IPASS.Chess import Ui_MainWindow


class TestSquareFunctions(unittest.TestCase):

    def testContainsPiece(self):
        # Test de containsPiece functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin staat op de square A1 een witte rook.
        self.assertEqual("white_rook_a", ui.squareA1.containsPiece().objectName())

        # In het begin staat op de square A5 niks.
        self.assertEqual(None, ui.squareA5.containsPiece())