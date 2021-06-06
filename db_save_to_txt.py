from app_config import *

for recipe in Recipe.query.all():
    with open(f'{recipe.name}.txt', 'w', encoding='utf-8') as f:
        s = ''
        s += f'{recipe.name}\n'
        s += f'{recipe.prepTime}\n'
        s += f'{recipe.cookingTime}\n'
        s += f'{recipe.servings}\n'
        s += f'{recipe.videoURL}\n'
        s += f'{recipe.sourceURL}\n'
        s += f'{recipe.tags}\n'
        s += f'{recipe.photo}\n'
        s += f'{recipe.favorite}\n'
        s += '### Steps ###\n'
        for line in recipe.steps.split('\n'):
            s += f'{line.strip()}\n'
        s += '### Ingredients ###\n'
        for ingredient in recipe.ingredients:
            s += f'{ingredient.amount} {ingredient.unit} {ingredient.name}\n'

        f.write(s)