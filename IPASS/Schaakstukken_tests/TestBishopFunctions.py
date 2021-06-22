import unittest
import sys

from PyQt5 import QtWidgets

from myRepository.IPASS.Chess import Ui_MainWindow


class TestBishopFunctions(unittest.TestCase):

    def testGetLegalMoves(self):
        # Test de getLegalMoves functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin kan de bishop niet bewegen en dus hoort de lijst leeg te zijn.
        self.assertEqual([], ui.black_bishop_c.getLegalMoves())

        # Als de bishop op F4 staat, dan kan hij naar 8 squares toe.
        ui.black_bishop_c.move(500, 400)
        self.assertEqual(8, len(ui.black_bishop_c.getLegalMoves()))

    def testBishopLongDiagonal(self):
        # Test de bishopLongDiagonal functie.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin is de bishop niet op de long diagonal, dus hoort het false te geven.
        self.assertEqual(False, ui.black_bishop_c.bishopLongdiagonal())

        # Als de bishop op F3 staat, dan staat hij op de long diagonal, dus hoort hij true te geven.
        ui.black_bishop_c.move(500, 500)
        self.assertEqual(True, ui.black_bishop_c.bishopLongdiagonal())

    def testGetValue(self):
        # Test de getValue functie van Bishop.
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # In het begin staat de bishop aan de buitenkant, dus hoort hij 29 punten te geven.
        self.assertEqual(29, ui.black_bishop_c.getValue())

        # Als de bishop op F4 staat, dan hoort hij 31 punten te geven.
        ui.black_bishop_c.move(500, 400)
        self.assertEqual(31, ui.black_bishop_c.getValue())

        # Als de bishop on de long diagonal zit, dan hoort hij 32 punten te geven
        ui.black_bishop_c.move(100, 600)
        self.assertEqual(32, ui.black_bishop_c.getValue())
