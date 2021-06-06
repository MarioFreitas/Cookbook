from app_config import *

@app.route('/recipe/<name>', methods=['POST', 'GET'])
@app.route('/recipe/<name>&scaling=<scaling>', methods=['POST', 'GET'])
def recipe(name, scaling=1):
    if request.method == 'POST':
        scaling = request.form['scaling']
        print('####', scaling)
    
    recipe = Recipe.query.get(name)

    try:
        servings = recipe.servings * float(scaling)
        if servings == int(servings):
            servings = int(servings)
    except:
        servings = ''

    amounts = []
    for ingredient in recipe.ingredients:
        amount = ingredient.amount * float(scaling)
        if amount == int(amount):
            amount = int(amount)
        amounts.append(amount)
    
    n_amounts = range(len(amounts))
    
    steps = recipe.steps.split('\n')
    return render_template('recipe.html', recipe=recipe, servings=servings, amounts=amounts, 
                           n_amounts=n_amounts, steps=steps, scaling=float(scaling), name=name)