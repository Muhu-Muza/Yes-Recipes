# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from flask import flash

class User():

    def __init__(self, firstname, lastname, email, username, password, confirm):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password
        self.confirm = confirm
        self.recipes = {}
        self.categories = {}

    def __repr__(self):
        return f'<User: {self.username}>'

    def add_category(self, category_name, description):
        if category_name not in self.categories:
            self.categories[category_name] = {}
            self.categories[category_name]["recipes"] = []
            self.categories[category_name]["description"] = description
        else:
            flash("Category Already Exists!")

    def edit_category(self, category_name, new_name, new_description):
        if category_name in self.categories:
            category_name = new_name
            self.categories[new_name]['description'] = new_description
        else:
            flash("Cannot process request! Category missing!")

    def delete_category(self, category_name):
        if category_name in self.categories:
            del self.categories[category_name]
        else:
            flash("Cannot process request! Category missing!")

    def create_recipe(self, recipe_name, category, ingredients, instructions):
        if recipe_name not in self.recipes:
            self.recipes[recipe_name] = {}
            self.recipes[recipe_name]["category"] = category
            self.recipes[recipe_name]["ingredients"] = ingredients
            self.recipes[recipe_name]["instructions"] = instructions
        else:
            flash("Food recipe already exists")

    def edit_recipe(self, recipe_name, new_name, new_category, new_ingredients, new_instructions):
        if recipe_name in self.recipes:
            recipe_name = new_name
            self.categories[new_name]['category'] = new_category
            self.categories[new_name]['ingredients'] = new_ingredients
            self.categories[new_name]['instructions'] = new_instructions
        else:
            flash("Cannot process request! Recipe missing!")

    def delete_recipe(self, recipe_name):
        if recipe_name in self.recipes:
            del self.recipes[recipe_name]
        else:
            flash("Cannot process request! Category missing!")