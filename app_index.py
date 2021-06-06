from app_config import *

@app.route('/', methods=['POST', 'GET'])
def index(category='All', favorite=False, tags=''):
    recipes = Recipe.query.order_by(Recipe.name)

    if request.method == 'POST':
        category = request.form.get('category')

        favorite = False
        if request.form.get('favorite') is not None:
            favorite = True
        
        tags = request.form['tags']
    
    if category != 'All':
        recipes = [i for i in recipes if category == i.category]

    if tags != '':
        recipes = [i for i in recipes if tags.lower() in i.tags.lower()]
    
    if favorite:
        recipes = [i for i in recipes if i.favorite]
    
    return render_template('index.html', recipes=recipes, category=category, 
                           favorite=favorite, tags=tags, categories=known_categories)