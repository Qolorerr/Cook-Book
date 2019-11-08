import sqlite3
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QTableWidgetItem


class OpenRecipeWindow(QWidget):
    def __init__(self, id):
        super().__init__()
        uic.loadUi('UI/RecipeView.ui', self)
        con = sqlite3.connect("DataBase.db")
        cur = con.cursor()
        request = 'SELECT * FROM Food WHERE id = {}'.format(id)
        id, name, recipe, image = cur.execute(request).fetchone()
        request = 'SELECT * FROM FoodIngredients WHERE Food = {}'.format(id)
        ingrInfo = cur.execute(request).fetchall()
        ingredients = []
        for i in range(len(ingrInfo)):
            request = 'SELECT ingredient FROM IngredientsName WHERE id = {}'
            ingredients.append([*ingrInfo[i]])
            ingredients[i][1] = cur.execute(request.format(ingrInfo[i][1])).fetchone()[0]
            ingredients[i][2] = str(ingredients[i][2])
            if ingredients[i][3] == '&':
                if ingredients[i][2] == '&':
                    ingredients[i][2] = ''
                    ingredients[i][3] = ''
                else:
                    ingredients[i][3] = 'items'
        con.close()
        self.name.setText(name)
        if image:
            filePATH = 'Images/' + str(id) + '.jpg'
            pixmap = QPixmap(filePATH)
            pixmap = pixmap.scaled(281, 281)
            self.image.setPixmap(pixmap)
        for i in range(len(ingredients)):
            self.ingredients.insertRow(i)
            self.ingredients.setItem(i, 0, QTableWidgetItem(ingredients[i][1]))
            self.ingredients.setItem(i, 1, QTableWidgetItem(ingredients[i][2]))
            self.ingredients.setItem(i, 2, QTableWidgetItem(ingredients[i][3]))
        self.recipe.setText(recipe)
