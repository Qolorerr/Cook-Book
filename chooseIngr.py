from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QCheckBox
import sqlite3

import addIngr


class ChooseIngrWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/ChooseIng.ui', self)
        f = open("buttonStyle.txt", "r")
        style = f.read()
        f.close()
        self.addIngr.setStyleSheet(style)
        self.refresh.setStyleSheet(style)
        self.addIngr.clicked.connect(self.add_ingr)
        self.refresh.clicked.connect(self.load_table)
        self.load_table()

    # Ingredients table building function
    def load_table(self):
        self.table.setRowCount(0)
        con = sqlite3.connect("DataBase.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM IngredientsName""").fetchall()
        con.close()
        for i in range(len(result)):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(result[i][1]))
            box = QCheckBox()
            box.setObjectName(str(result[i][0]))
            box.setChecked(result[i][2] == 1)
            self.table.setCellWidget(i, 1, box)
            box.stateChanged.connect(self.change_alailability)

    # CheckBox processing in ingredients table
    def change_alailability(self):
        id = self.sender().objectName()
        newValue = self.sender().isChecked()
        con = sqlite3.connect("DataBase.db")
        cur = con.cursor()
        request = "UPDATE IngredientsName SET availability = {} WHERE id = {}"
        cur.execute(request.format(newValue, id))
        con.commit()
        con.close()

    # Open ADD INGREDIENT window
    def add_ingr(self):
        self.showAIW = addIngr.AddIngrWindow()
        self.showAIW.show()
