import unittest
import sys

from PyQt5 import QtWidgets

from myRepository.IPASS.Chess import Ui_MainWindow


class TestChesspieceFunctions(unittest.TestCase):

    def testGetPosition(self):
        # Test de getPosition functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin is de positie van de zwarte koning E8
        self.assertEqual("squareE8", ui.black_king.getPosition().objectName())

        # In het begin is de positie van de witte queen D1
        self.assertEqual("squareD1", ui.white_queen.getPosition().objectName())