from app_config import *

@app.route('/edit/<name>', methods=['POST', 'GET'])
def edit(name):
    if request.method == 'GET':
        recipe = Recipe.query.get(name)

        amounts = []
        for ingredient in recipe.ingredients:
            amount = ingredient.amount
            amounts.append(amount)
        
        n_amounts = range(len(amounts))
        
        return render_template('edit.html', recipe=recipe, amounts=amounts, 
                               n_amounts=n_amounts, new=False, categories = known_categories)
    
    elif request.method == 'POST':
        recipe = Recipe.query.get(name)
        nameOld = recipe.name

        recipe.name = request.form['name']
        recipe.prepTime = request.form['prepTime']
        recipe.cookingTime = request.form['cookingTime']
        recipe.servings = request.form['servings']
        recipe.videoURL = request.form['videoURL']
        recipe.sourceURL = request.form['sourceURL']
        recipe.category = request.form.get('category')
        recipe.tags = request.form['tags']

        favorite = request.form.get('favorite')
        if favorite == '0':
            recipe.favorite = False
        else:
            recipe.favorite = True

        recipe.steps = request.form['steps']

        if request.files['file'].filename != '':
            photo_file = request.files['file']
            _, extension = os.path.splitext(photo_file.filename)
            photo = f'./static/img/{name}{extension}'
            photo_file.save(photo)    
            recipe.photo = photo
        
        db.session.commit()

        for ingredient in recipe.ingredients:
            db.session.delete(ingredient)

        if recipe.name != nameOld:
            for ingredient in Ingredient.query.all():
                if ingredient.recipe_name == name:
                    db.session.delete(ingredient)
        db.session.commit()
        
        ingredients = request.form['ingredients']
        ingredients = ingredients.split('\n')
        for line in ingredients:
            if line.strip() in ['', '\n', '\r']:
                continue
            l = line.split()

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

        return redirect(f'/recipe/{recipe.name}')