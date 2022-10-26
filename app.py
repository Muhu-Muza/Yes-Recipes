# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from functools import wraps
import os
#  lists out the files and directories present provides functions for creating,removing fetching contents of a directory (folder) 
#  This module provides a portable way of using operating system dependent functionality by establishing an
#  interaction between the user and the operating system
from flask import (Flask, render_template, request, session, url_for, redirect, flash)
# import models
from models import User




app = Flask(__name__)
app.secret_key = os.urandom(32)
app.debug = True
users = {}





def login_is_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        flash('You are not authorised to access this page, Please log in!')
        return redirect(url_for('login'))
    return wrapper

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        if username in users:
            flash('That user already exists')
        else:
            if password != confirm:
                flash('The two passwords you entered are not the same')
            else:
                if password == confirm:
                    user = User( firstname, lastname, email, username, password, confirm)
                    users[user.username] = user
                    flash('User Added Succesfully')
                    return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] not in users:
            flash('User not recognised. Please register!')
        else:
            username = request.form['username']
            user = users.get(username)
            if request.form['password'] not in user.password:
                flash('Incorrect password')
            else:
                session['logged_in'] = True
                session['username'] = request.form['username']
                return redirect(url_for('dashboard', username = username))
    return render_template('login.html')

@app.route('/logout')
@login_is_required
def logout():
    session.pop('logged_in', None)
    flash('You Have Logged out, Login to Continue !')
    return redirect(url_for('login'))

@app.route('/<username>/dashboard')
@login_is_required
def dashboard(username):
    user = users[username]
    the_user = user.username
    return render_template('dashboard.html', the_user = the_user)

@app.route('/<username>/create_category', methods=['GET','POST'])
@login_is_required
def create_category(username):
    user = users[username]
    username = user.username
    if request.method == "POST":
        category_name = request.form['category']
        description = request.form['description']      
        if category_name in user.categories:
            flash('Category already exists')
        else:
            user.add_category(category_name, description)
            return redirect(url_for('categories', username = username))
    return render_template('create_category.html', username = username)

@app.route("/edit_category/<category_name>", methods = ['GET', 'POST'])
@login_is_required
def edit_category(category_name):
    if request.method =="POST":
        new_name = request.form['category']
        new_description = request.form['description']
        if new_name:
            user = users[session['username']]           
            user.add_category(new_name, new_description)
            user.categories[new_name] = user.categories[category_name]
            user.categories[new_name]["new_description"] = user.categories[category_name]["description"]
            user.delete_category(category_name)
            username = user.username
            return redirect(url_for('categories', username = username))
    return render_template('edit_category.html', category_name = category_name)

@app.route('/delete_category/<name>')
@login_is_required
def delete_category(name):
    usr = users[session['username']]
    usr.delete_category(name)
    return redirect(url_for('user', username=usr.username))

@app.route("/<username>/categories")
def categories(username):
    user = users[username]
    username = user.username
    the_categories = user.categories
    return render_template('my_categories.html', the_categories = the_categories, username = username)



if __name__ == "__main__":
    app.run()
