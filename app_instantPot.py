from app_config import *

@app.route('/Instant-Pot', methods=['POST', 'GET'])
def instantPot():
    recipes = InstantPot.query.order_by(InstantPot.name)
    return render_template('instantPot.html', recipes=recipes)

@app.route('/Instant-Pot/New', methods=['POST', 'GET'])
def instantPot_New():
    if request.method == 'GET':
        return render_template('instantPot_Edit.html', new=True)

    if request.method == 'POST':
        name = request.form['name']
        method = request.form['method']
        water = request.form['water']
        quantity = request.form['quantity']
        time = request.form['time']
        venting = request.form['venting']
        notes = request.form['notes']

        recipe = InstantPot(name=name, method=method, water=water, quantity=quantity, time=time, venting=venting, notes=notes)

        db.session.add(recipe)
        db.session.commit()

        return redirect(f'/Instant-Pot')

@app.route('/Instant-Pot/Edit/<name>', methods=['POST', 'GET'])
def instantPot_Edit(name):
    recipe = InstantPot.query.get(name)

    if request.method == 'GET':
        return render_template('instantPot_Edit.html', new=False, recipe=recipe)

    if request.method == 'POST':
        recipe.name = request.form['name']
        recipe.method = request.form['method']
        recipe.water = request.form['water']
        recipe.quantity = request.form['quantity']
        recipe.time = request.form['time']
        recipe.venting = request.form['venting']
        recipe.notes = request.form['notes']

        db.session.commit()

        return redirect(f'/Instant-Pot')