# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from functools import (wraps)
import os
from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_migrate import Migrate
from datetime import datetime
from wtforms.widgets import TextArea

import user_model




# app = Flask(__name__)
# app.debug = True
# app.secret_key = os.urandom(32)



# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key = True)
#     firstname = db.Column(db.String(20), nullable = False)
#     lastname = db.Column(db.String(20), nullable = False)
#     username = db.Column(db.String(20), nullable = False, unique = True)
#     email = db.Column(db.String(30), nullable = False)
#     password_hash = db.Column(db.String(100), nullable = False)
#     recipes = db.relationship('Recipe', backref = 'creater')
#     categories = db.relationship('Category', backref = 'poster')
    
#     @property
#     def password(self):
#         raise AttributeError('Password is not a readable attribute!')
#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)
            
#     def __repr__(self):
#         return '<User %r>' % self.username


# class Recipe(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.Text(80))
#     # category = db.Column(db.String(50))
#     category = db.Column(db.Integer, db.ForeignKey('category.id'))
#     ingredients = db.Column(db.String(500))
#     instructions = db.Column(db.String(500))
#     date_posted = db.Column(db.DateTime, default = datetime.utcnow)
#     creater_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.Text(80), unique=True, nullable = False)
#     description = db.Column(db.String(200))
#     recipes = db.relationship('Recipe', backref = 'poster')
#     poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # person_id = db.Column(db.Integer, db.ForeignKey('person.id'),nullable=False)


class RegisterForm(FlaskForm):
    firstname = StringField("First Name", validators = [InputRequired(), Length (min = 3, max = 20)])
    lastname = StringField("Last Name", validators = [InputRequired(), Length (min = 3, max = 20)])
    email = StringField("Email", validators = [InputRequired()])
    username = StringField("Username", validators = [InputRequired(), Length (min = 4, max = 20)])
    password_hash = PasswordField("Password", validators = [InputRequired(), EqualTo('password_hash2', message = 'Passwords Must Match'), Length (min=8, max=20)])
    password_hash2 = PasswordField("confirm password", validators = [InputRequired(), Length (min = 8, max = 20)])
    # submit = SubmitField("Submit")

    # def validate_username(self, username):
    #         existing_username = User.query.filter_by(username = username.data).first()
    #         if existing_username:
    #                 raise ValidationError(
    #                         "Username already exists. Please choose a different one!"
    #                 )


class LoginForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired(), Length (min = 4, max = 20)])
    password = PasswordField("Password", validators = [InputRequired(), Length (min = 8, max = 20)])
    # submit = SubmitField("Login")


# class RecipeForm(FlaskForm):

#     with app.app_context():
#         cat = Category.query.order_by(Category.title).all()
    
#     title = StringField("Title", validators = [InputRequired()])
#     category = SelectField("Category", choices = cat)
#     ingredients = StringField("Instructions", validators = [InputRequired()], widget = TextArea())
#     instructions = StringField("Instructions", validators = [InputRequired()], widget = TextArea())
    # submit = SubmitField("Submit")


# class CategoryForm(FlaskForm):
#     title = StringField("Title", validators = [InputRequired(), Length(min = 4, max = 30)])
#     description = StringField("Description", validators = [InputRequired()], widget = TextArea())

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)

        flash('You are not authorised to access this page, Please log in!')
        return redirect(url_for('login'))
    return wrapper

@app.route("/")
def index():
    
    return render_template('index.html')

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal server Eerror
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

@app.route("/dashboard")
@login_required
def dashboard():
    
    return render_template('dashboard.html')

@app.route("/signup", methods=(['GET', 'POST']))
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        username = form.username.data
        confirm_password = form.confirm_password.data
        add_user = user_model.Users(
                    firstname,
                    lastname,
                    email,
                    username,
                    confirm_password
                    )
        add_user.sign_up()
        
        flash("User Added Succesfully")             
        return redirect(url_for('login'))

    return render_template('signup.html', form = form)
         
@app.route("/login", methods=(['GET', 'POST']))
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        for username in user_model.registered_users:
            if username == username and password == password:
                return redirect(url_for('dashboard'))

    return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You Have Logged out, Login to Continue !')
    return redirect(url_for('login'))

# @app.route("/create-recipe", methods=['GET','POST'])
# @login_required
# def create_recipe():

#     form = RecipeForm()
#     # kategory = Category.query.order_by(Category.title).all()
#     if form.validate_on_submit():
#         the_creater = current_user.id
#         recipe = Recipe(
#             title = form.title.data,
#             category = form.category.data,
#             ingredients = form.ingredients.data,
#             instructions = form.instructions.data,
#             creater_id = the_creater
#             )

#         db.session.add(recipe)
#         db.session.commit()
#         flash("Recipe added successfully!")
#         return redirect(url_for('view_recipes'))     

#     return render_template('create-recipe.html', form = form)

# @app.route("/view-recipes")
# def view_recipes():
#     recipes = Recipe.query.order_by(Recipe.date_posted)
#     return render_template('recipes.html', recipes = recipes)

# @app.route("/my_recipes")
# def my_recipes():
#     user = User.query.filter_by(username = current_user.username).first_or_404() 
#     recipes = user.recipes
#     return render_template('my_recipes.html', recipes = recipes, user = user)

# @app.route('/my_recipes/edit/<int:id>', methods = ['GET','POST'])
# @login_required
# def edit_recipe(id):
#     recipe = Recipe.query.get_or_404(id)
#     form = RecipeForm()
#     if form.validate_on_submit():
#         recipe.title = form.title.data
#         recipe.category = form.category.data
#         recipe.ingredients = form.ingredients.data
#         recipe.instructions = form.instructions.data

#         db.session.add(recipe)
#         db.session.commit()
#         flash("Recipe has been updated!")
#         return redirect(url_for('my_recipes', id = recipe.id))

#     form.title.data = recipe.title 
#     form.category.data = recipe.category 
#     form.ingredients.data = recipe.ingredients 
#     form.instructions.data = recipe.instructions 
#     return render_template('edit_recipe.html', form = form)

# @app.route('/my_recipes/delete/<int:recipe_id>')
# @login_required
# def delete_recipe(recipe_id):
#     recipe_to_delete = Recipe.query.get_or_404(recipe_id)
#     db.session.delete(recipe_to_delete)
#     db.session.commit()
#     flash("Recipe has been Deleted!")
#     return redirect(url_for('my_recipes', recipe_id = recipe_to_delete.id))

# @app.route("/create-category", methods = ["GET", "POST"])
# @login_required
# def create_category():
#     form = CategoryForm()
#     if form.validate_on_submit():
#         the_poster = current_user.id
#         category = Category(
#                 title = form.title.data,
#                 description = form.description.data,
#                 poster_id = the_poster
#                 )

#         db.session.add(category)
#         db.session.commit()
#         flash("Category Added Successfully!")
#         return redirect(url_for('categories'))
#     return render_template('create_category.html', form = form )

# @app.route("/categories")
# def categories():
#     categories = Category.query.order_by(Category.id).all()
#     return render_template('categories.html', categories=categories)

# @app.route("/edit-category/<int:id>", methods = ["GET", "POST"])
# @login_required
# def edit_category(id):
#     category = Category.query.get_or_404(id)
#     form = CategoryForm()
#     if form.validate_on_submit():
#         category.title = form.title.data
#         category.description = form.description.data

#         db.session.add(category)
#         db.session.commit()
#         flash("Category Updated Successfully!")
#         return redirect(url_for('categories', id = category.id))
#     form.title.data = category.title
#     form.description.data = category.description
#     return render_template('edit_category.html', form = form)



# @app.route('/my_categories/delete/<int:category_id>')
# @login_required
# def delete_category(category_id):
#     category_to_delete = Category.query.get_or_404(category_id)
#     db.session.delete(category_to_delete)
#     db.session.commit()
#     flash("Category has been Deleted!")
#     return redirect(url_for('my_categories', category_id = category_to_delete.id))

# @app.route("/my_categories")
# def my_categories():
#     user = User.query.filter_by(username = current_user.username).first_or_404() 
#     categories = user.categories
#     return render_template('my_categories.html', categories = categories, user = user)

# @app.route("/category-detail/<int:id>")
# def category_detail(id):
#     category_detail = Category.query.get_or_404(id)
#     return render_template('category_detail.html', id = category_detail.id, )






# if __name__ == "__main__":
#     app.run()




