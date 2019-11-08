"""
Cook Book v1.0
Data base: 59 elements

Author: Ivanov Mihail
Logo creator: Kiprianov Ivan
"""


import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

import chooseIngr
import findRecipe
import addRecipe


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/Main.ui', self)
        f = open("buttonStyle.txt", "r")
        style = f.read().replace('10', '12')
        f.close()
        self.findB.setStyleSheet(style)
        self.addB.setStyleSheet(style)
        self.chooseB.setStyleSheet(style)
        pixmap = QPixmap("logo.png")
        pixmap = pixmap.scaled(151, 121)
        self.image.setPixmap(pixmap)
        self.findB.clicked.connect(self.find_recipe)
        self.addB.clicked.connect(self.add_recipe)
        self.chooseB.clicked.connect(self.choose_ingr)

    # Open RECIPES window
    def find_recipe(self):
        self.showFRW = findRecipe.ListRecipeWindow()
        self.showFRW.show()

    # Open ADD RECIPE window
    def add_recipe(self):
        self.showARW = addRecipe.AddRecipeWindow()
        self.showARW.show()

    # Open CHOOSE AVAILABLE INGREDIENTS window
    def choose_ingr(self):
        self.showCIW = chooseIngr.ChooseIngrWindow()
        self.showCIW.show()


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())
