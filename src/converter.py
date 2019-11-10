import sqlite3


f = open("res/recipes.txt", mode="r", encoding="utf-16")
data = str(f.read()).split('INSERT INTO `recipes` VALUES ')[51:60]
f.close()
units = set()
f = open("res/units.txt", "r")
for i in f.read().split('\n'):
    units.add(i)
f.close()
con = sqlite3.connect("res/DataBase.db")
cur = con.cursor()
ingr = set()
for i in cur.execute("SELECT Ingredient FROM IngredientsName").fetchall():
    ingr.add(i)
print(ingr)
for i in data:
    id = cur.execute("""SELECT MAX(id) FROM Food""").fetchone()[0] + 1
    value = '[' + i[1:-3] + ']'
    value = eval(value)[:-3]
    name = value[1].strip()
    recipe = value[4]
    image = False
    for j in value[3].split(', '):
        x = j.split()
        count = x[0]
        unit = x[1]
        units.add(unit)
        ing = ' '.join(x[2:]).lower()
        if ing in ingr:
            request = "SELECT id FROM IngredientsName WHERE ingredient = '{}'"
            ingID = cur.execute(request.format(ing)).fetchone()[0]
        else:
            ingID = cur.execute("""SELECT MAX(id) FROM IngredientsName""").fetchone()[0] + 1
            request = "INSERT INTO IngredientsName VALUES({}, '{}', False)"
            request = request.format(ingID, ing)
            try:
                cur.execute(request)
            except:
                print(request + '\n' + ing + '\n' + str(ingr))
        request = "INSERT INTO FoodIngredients VALUES({}, {}, '{}', '{}')"
        cur.execute(request.format(id, ingID, count, unit))
        ingr.add(ing)
    request = "INSERT INTO Food VALUES({}, '{}', '{}', {})"
    cur.execute(request.format(id, name, recipe, image))
f = open("res/units.txt", "w")
f.write('\n'.join([*units]))
f.close()
con.commit()
con.close()