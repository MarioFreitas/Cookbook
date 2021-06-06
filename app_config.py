from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_NATIVE_UNICODE'] = 'utf8mb4'

known_units = ['g', 'kg', 'mg', 'lb', 'l', 'ml', 'tsp', 'tbsp', 
               'teaspoon', 'teaspoons', 'tablespoon', 'tablespoon', 
               'cup', 'cups', 'quart', 'quarts', 'can', 'cans',
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

if __name__ == '__main__':
    db.create_all()
    print('database created')