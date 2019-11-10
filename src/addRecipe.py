import sqlite3
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtWidgets import QCheckBox, QFileDialog, QComboBox
from PIL import Image

import src.addIngr as addIngr


class AddRecipeWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('res/UI/AddRecipe.ui', self)
        self.load_table()
        self.imageName = ''
        self.ingredients = set()
        f = open("res/buttonStyle.txt", "r")
        style = f.read()
        f.close()
        self.addIngr.setStyleSheet(style)
        self.refresh.setStyleSheet(style)
        self.openImage.setStyleSheet(style)
        self.save.setStyleSheet(style.replace('10', '12'))
        self.addIngr.clicked.connect(self.add_ingr)
        self.refresh.clicked.connect(self.load_table)
        self.openImage.clicked.connect(self.open_image)
        self.save.clicked.connect(self.save_recipe)

    # Ingredients table building function
    def load_table(self):
        self.table.setRowCount(0)
        con = sqlite3.connect("res/DataBase.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM IngredientsName""").fetchall()
        con.close()
        for i in range(len(result)):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(result[i][1]))
            self.table.setItem(i, 2, QTableWidgetItem(''))
            box = QCheckBox()
            box.setObjectName(str(result[i][0]))
            self.table.setCellWidget(i, 1, box)
            box.stateChanged.connect(self.change_require)
            units = QComboBox()
            f = open('res/units.txt', 'r')
            units.addItems(f.read().split('\n'))
            f.close()
            units.setObjectName(str(result[i][0]))
            self.table.setCellWidget(i, 3, units)

    # Image opening function
    def open_image(self):
        title = 'Choose image'
        formats = "Images (*.png *.jpg *.bmp)"  # You can use only PNG, JPG, BMP formats
        imageName = QFileDialog.getOpenFileName(self, title, '', formats)[0]
        if imageName is None:
            return
        self.imageName = imageName
        pixmap = QPixmap(imageName)
        pixmap = pixmap.scaled(251, 251)
        self.imageView.setPixmap(pixmap)

    # CheckBox processing in ingredients table
    def change_require(self):
        id = self.sender().objectName()
        if self.sender().isChecked():
            self.ingredients.add(id)
        else:
            self.ingredients.discard(id)

    # Open ADD INGREDIENT window
    def add_ingr(self):
        self.showAIW = addIngr.AddIngrWindow()
        self.showAIW.show()

    # Save all filled data in data base
    def save_recipe(self):
        name = self.name.text()
        recipe = self.recipe.toPlainText()
        con = sqlite3.connect("res/DataBase.db")
        cur = con.cursor()
        id = cur.execute("""SELECT MAX(id) FROM Food""").fetchone()[0] + 1
        image = False
        if self.imageName != '':
            im = Image.open(self.imageName)
            filePath = 'Images/' + str(id) + '.jpg'
            im.save(filePath)
            image = True
        ingredients = sorted([*self.ingredients])
        for i in range(len(ingredients)):
            ingID = int(ingredients[i])
            count = self.table.item(ingID, 3).text()
            unit = self.table.cellWidget(ingID, 4).currentText()
            if unit == 'items':
                unit = '&'
            if count == '':
                count = '&'
                unit = '&'
            request = "INSERT INTO FoodIngredients VALUES({}, {}, '{}' , '{}')"
            cur.execute(request.format(id, ingID, count, unit))
        request = "INSERT INTO Food VALUES({}, '{}', '{}' , {})"
        cur.execute(request.format(id, name, recipe, image))
        con.commit()
        con.close()
        self.close()
