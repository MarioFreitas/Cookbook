from app_config import *

# name = 'Beef Stew2'

# recipe = Recipe.query.get(name)

# try:
#     db.session.delete(recipe)
# except:
#     pass

# for ingredient in Ingredient.query.all():
#     if ingredient.recipe_name == name:
#         db.session.delete(ingredient)
# db.session.commit()

db.drop_all()