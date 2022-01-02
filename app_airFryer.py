from app_config import *

@app.route('/Air-Fryer', methods=['POST', 'GET'])
def airFryer():
    recipes = AirFryer.query.order_by(AirFryer.name)
    return render_template('airFryer.html', recipes=recipes)

@app.route('/Air-Fryer/New', methods=['POST', 'GET'])
def airFryer_New():
    if request.method == 'GET':
        return render_template('airFryer_Edit.html', new=True)

    if request.method == 'POST':
        name = request.form['name']
        temperature = request.form['temperature']
        time = request.form['time']
        notes = request.form['notes']

        recipe = AirFryer(name=name, temperature=temperature, time=time, notes=notes)

        db.session.add(recipe)
        db.session.commit()

        return redirect(f'/Air-Fryer')

@app.route('/Air-Fryer/Edit/<name>', methods=['POST', 'GET'])
def airFryer_Edit(name):
    recipe = AirFryer.query.get(name)

    if request.method == 'GET':
        return render_template('airFryer_Edit.html', new=False, recipe=recipe)

    if request.method == 'POST':
        recipe.name = request.form['name']
        recipe.temperature = request.form['temperature']
        recipe.time = request.form['time']
        recipe.notes = request.form['notes']

        db.session.commit()

        return redirect(f'/Air-Fryer')