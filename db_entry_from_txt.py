from app_config import *

# db.drop_all()
# db.create_all()

with open('Moqueca de peixe.txt', 'r', encoding='utf-8') as f:
    name = f.readline().strip()
    prepTime = f.readline().strip()
    cookingTime = f.readline().strip()
    servings = f.readline().strip()
    videoURL = f.readline().strip()
    sourceURL = f.readline().strip()
    category = f.readline().strip()
    tags = f.readline().strip()
    photo = f.readline().strip()
    favorite = eval(f.readline().strip())
    f.readline().strip()

    steps = ''
    while True:
        line = f.readline()
        if line[0:3] == '###':
            break
        steps += line

    recipe = Recipe(name=name, prepTime=prepTime, cookingTime=cookingTime, 
                    servings=servings, videoURL=videoURL, sourceURL=sourceURL, 
                    category=category, tags=tags, photo=photo, favorite=favorite, steps=steps)
    
    db.session.add(recipe)
    db.session.commit()

    for line in f:
        l = line.split(' ')
        amount = 0
        unit = ''
        amount_skip = 0
        unit_skip = 0
        try:
            amount = float(l[0])
            amount_skip = len(l[0]) + 1

            if l[1] in known_units:
                unit = l[1]
                unit_skip = len(l[1]) + 1
        except:
            pass
        
        name = line[amount_skip + unit_skip:].strip()
        
        ingredient = Ingredient(name=name, amount=amount, unit=unit, recipe_name=recipe.name)
        db.session.add(ingredient)
        db.session.commit()

