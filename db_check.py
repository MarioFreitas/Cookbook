from app_config import *

# ingredients = Ingredient.query.all()
# for ingredient in ingredients:
#     print(ingredient)

print(Recipe.query.get('Beef Stew').category)