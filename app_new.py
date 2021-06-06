from app_config import *

@app.route('/new/', methods=['POST', 'GET'])
def new():
    if request.method == 'GET':
        return render_template('edit.html', new=True, categories=known_categories)
    
    elif request.method == 'POST':
        name = request.form['name']
        prepTime = request.form['prepTime']
        cookingTime = request.form['cookingTime']
        servings = request.form['servings']
        videoURL = request.form['videoURL']
        sourceURL = request.form['sourceURL']
        category = request.form.get('category')
        tags = request.form['tags']

        favorite = request.form.get('favorite')
        if favorite == '0':
            favorite = False
        else:
            favorite = True

        steps = request.form['steps']

        if request.files['file'].filename != '':
            photo_file = request.files['file']
            _, extension = os.path.splitext(photo_file.filename)
            photo = f'./static/img/{name}{extension}'
            photo_file.save(photo)    
            photo = photo
        else:
            photo=''
        
        recipe = Recipe(name=name, prepTime=prepTime, cookingTime=cookingTime, 
                    servings=servings, videoURL=videoURL, sourceURL=sourceURL, 
                    category=category,tags=tags, photo=photo, favorite=favorite, steps=steps)
        db.session.add(recipe)
        db.session.commit()

        ingredients = request.form['ingredients']
        ingredients = ingredients.split('\n')
        for line in ingredients:
            if line.strip() in ['', '\n', '\r']:
                continue
            l = line.split()
            print(l)

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
