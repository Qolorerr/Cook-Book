import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QPushButton

import openRecipe


class ListRecipeWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/RecipeList.ui', self)
        f = open("buttonStyle.txt", "r")
        style = f.read().replace('10', '12')
        f.close()
        self.refresh.setStyleSheet(style)
        self.refresh.clicked.connect(self.load_table)
        self.load_table()

    # Recipes table building function
    def load_table(self):
        self.table.setRowCount(0)
        con = sqlite3.connect("DataBase.db")
        cur = con.cursor()
        result = cur.execute("""SELECT id, Name FROM Food""").fetchall()
        recipes = []
        if self.filter.isChecked():
            request = "SELECT id FROM IngredientsName WHERE availability = 1"
            ingredients = cur.execute(request).fetchall()
            ingrAvail = set()
            for i in range(len(ingredients)):
                ingrAvail.add(ingredients[i][0])
            for i in range(len(result)):
                id = result[i][0]
                request = 'SELECT Ingredient FROM FoodIngredients WHERE Food = {}'
                ingredients = cur.execute(request.format(id)).fetchall()
                needIngr = set()
                for j in range(len(ingredients)):
                    needIngr.add(ingredients[j][0])
                if needIngr <= ingrAvail:
                    recipes.append(result[i])
        else:
            recipes = result
        con.close()
        for i in range(len(recipes)):
            self.table.insertRow(i)
            button = QPushButton()
            button.setObjectName(str(recipes[i][0]))
            button.setText(recipes[i][1])
            self.table.setCellWidget(i, 0, button)
            button.clicked.connect(self.open_recipe)

    # Open recipe click processing
    def open_recipe(self):
        id = self.sender().objectName()
        self.showRVW = openRecipe.OpenRecipeWindow(id)
        self.showRVW.show()
