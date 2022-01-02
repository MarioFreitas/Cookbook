from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
app.config['SQLALCHEMY_BINDS'] = {'airFryer' : 'sqlite:///airFryer.db',
                                  'instantPot': 'sqlite:///instantPot.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_NATIVE_UNICODE'] = 'utf8mb4'

known_units = ['g', 'gram', 'grams', 
               'kg', 'kilo', 'kilos', 'kilogram', 'kilograms', 
               'mg', 'miligram', 'miligrams', 
               'lb', 'pound', 'pounds',
               'l', 'L', 'liter', 'liters',
               'ml', 'mL', 'mililiter', 'mililiters',
               'tsp', 'teaspoon', 'teaspoons', 'c. à thé',
               'tbsp', 'tablespoon', 'tablespoons', 'c. à table',
               'cup', 'cups', 'tasse', 'tasses', 'de tasse'
               'quart', 'quarts', 
               'can', 'cans',
               'bottle', 'bottles']

known_categories = ['Bread', 'Desert', 'Main dish', 'Salad', 'Snack', 'Soup', 'Others']

db = SQLAlchemy(app)

class Recipe(db.Model):
    name = db.Column(db.String, nullable=False, unique=True, primary_key=True)
    prepTime = db.Column(db.String, nullable=False)
    cookingTime = db.Column(db.String, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    videoURL = db.Column(db.String, nullable=False)
    sourceURL = db.Column(db.String, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String, nullable=False)
    favorite = db.Column(db.Boolean, default=False)
    category = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=False)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)

    def __repr__(self):
        return f'<Recipe {self.name}>'

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, default=0)
    unit = db.Column(db.String, default='')
    recipe_name = db.Column(db.String, db.ForeignKey('recipe.name'), nullable=False)

    def __repr__(self):
        return f'<Ingredient {self.id}: {self.recipe_name} - {self.name}>'

class AirFryer(db.Model):
    __bind_key__ = 'airFryer'
    name = db.Column(db.String, nullable=False, unique=True, primary_key=True)
    temperature = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<AirFryer {self.name}>'

class InstantPot(db.Model):
    __bind_key__ = 'instantPot'
    name = db.Column(db.String, nullable=False, unique=True, primary_key=True)
    method = db.Column(db.String, nullable=False)
    water = db.Column(db.String, nullable=False)
    quantity = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    venting = db.Column(db.String, nullable=True)
    notes = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<InstantPot {self.name}>'

if __name__ == '__main__':
    db.create_all()
    db.create_all(bind='airFryer')
    db.create_all(bind='instantPot')
    # beans = InstantPot(name='Black Beans (Dry)', method='Pressure High', water='cover', quantity='2 cups', time='20 mins', venting='Quick Release', notes=None)
    # db.session.add(beans)
    # db.session.commit()
    print('database created')