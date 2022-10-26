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
        self.recipe = {}
        self.categories = {}

    def __repr__(self):
        return f'<User: {self.username}>'

    def add_category(self, category_name, description):
        if category_name not in self.categories:
            self.categories[category_name] = {}
            self.categories[category_name]["recipes"] = []
            self.categories[category_name]["description"] = description

            # {"juice": {
            #             recipes: [mango, tea tree juice]
            #             description: "wewewe"
            #             }}

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

    def create_recipe(self, category_name, recipe_name, ingredients = """ """, instructions = """ """ ):
        if category_name in self.categories:
            self.categories[category_name].append(recipe_name)
            if recipe_name not in self.recipe:
                ingredients = ingredients.split("r\n")
                instructions = instructions.split("\r\n")
                self.recipe[recipe_name] = instructions
                self.recipe[recipe_name] = ingredients
            else:
                flash("Food recipe already exists")

    def view(self, recipe_name):
        if recipe_name in self.recipe:
            return self.recipe[recipe_name]
        else:
            flash("Recipe Doesn't exist!")

    def update(self, recipe_name, new_name):
        if recipe_name in self.recipe:
            self.recipe[new_name] = self.recipe[recipe_name]
            del self.recipe[recipe_name]
        else:
            flash("Recipe Doesn't exist!")

    def delete(self, recipe_name):
        if recipe_name in self.recipe:
            del self.recipe[recipe_name]
        else:
            flash("Invalid Request")