import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QErrorMessage


class AddIngrWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/AddIng.ui', self)
        f = open("buttonStyle.txt", "r")
        style = f.read().replace('10', '12')
        f.close()
        self.pushButton.setStyleSheet(style)
        self.pushButton.clicked.connect(self.save_ingr)
        self.error = QErrorMessage()

    # Save ingredient in data base
    def save_ingr(self):
        name = self.name.text()
        con = sqlite3.connect("DataBase.db")
        cur = con.cursor()
        request = "INSERT INTO IngredientsName(ingredient) VALUES('{}')"
        try:
            cur.execute(request.format(name))
            con.commit()
            con.close()
            self.close()
        except:
            self.error.showMessage('This ingredient already exist')
            con.close()
