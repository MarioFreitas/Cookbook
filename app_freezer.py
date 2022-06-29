from app_config import *

@app.route('/Freezer/Filter/<category>/<tags>/<order>/<quantityFilter>', methods=['POST', 'GET'])
def freezer_filter(category='All', tags='', order='Name', quantityFilter='Show All'):
    if order == 'Quantity':
        items = Freezer.query.order_by(Freezer.category, Freezer.quantity, Freezer.name)
    else:
        items = Freezer.query.order_by(Freezer.category, Freezer.name)

    cat_Beef = Freezer(name='Beef', quantity=-1, unit='', category='Category')


    if category != 'All':
        items = [i for i in items if category == i.category]

    if tags == '' or tags == 'none':
        tags = 'none'
    else:
        items = [i for i in items if (tags.lower() in i.name.lower())]

    if quantityFilter == 'Show Only Zeroes':
        items = [i for i in items if i.quantity == 0]
    elif quantityFilter == 'Show Only Non-Zeroes':
        items = [i for i in items if i.quantity != 0]

    return render_template('freezer.html', items=items, category=category, tags=tags, categories=freezer_cateogries, order=order, quantityFilter=quantityFilter)

@app.route('/Freezer', methods=['POST', 'GET'])
def freezer(category='All', tags='none', order='Name', quantityFilter='Show All'):
    if request.method == 'POST':
        category = request.form.get('category')
        tags = request.form['tags']
        if tags == '':
            tags = 'none'
        order = request.form.get('order')
        quantityFilter = request.form.get('quantityFilter')

        return redirect(f'Freezer/Filter/{category}/{tags}/{order}/{quantityFilter}')

    return redirect(f'Freezer/Filter/{category}/{tags}/{order}/{quantityFilter}')

@app.route('/Freezer/New', methods=['POST', 'GET'])
def freezer_New():
    if request.method == 'GET':
        return render_template('freezer_edit.html', new=True, categories = freezer_cateogries)

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        unit = request.form['unit']
        category = request.form['category']

        item = Freezer(name=name, quantity=quantity, unit=unit, category=category)

        db.session.add(item)
        db.session.commit()

        return redirect(f'/Freezer')

@app.route('/Freezer/Edit/<name>', methods=['POST', 'GET'])
def freezer_Edit(name):
    item = Freezer.query.get(name)

    if request.method == 'GET':
        return render_template('freezer_edit.html', new=False, item=item, categories = freezer_cateogries)

    if request.method == 'POST':
        item.name = request.form['name']
        item.quantity = request.form['quantity']
        item.unit = request.form['unit']
        item.category = request.form['category']

        db.session.commit()

        return redirect(f'/Freezer')

@app.route('/Freezer/Filter/<category>/<tags>/<order>/<quantityFilter>/<name>/<sign>', methods=['POST', 'GET'])
def freezer_PlusMinus(category, tags, order, quantityFilter, name, sign):
    item = Freezer.query.get(name)

    if request.method == 'GET':
        if sign == 'Plus':
            item.quantity += 1
        elif sign == 'Minus':
            item.quantity -= 1
            if item.quantity < 0:
                item.quantity = 0

        db.session.commit()

        return redirect(f'/Freezer/Filter/{category}/{tags}/{order}/{quantityFilter}')