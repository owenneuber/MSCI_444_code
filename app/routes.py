# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:39:03 2020

@author: Owen
"""

from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from models import Users, Suppliers, Orders, InventoryInOrder, InventoryItems
from sqlalchemy.orm import sessionmaker
#engine = create_engine(DATABASE_URI)
#session = Session()

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)



"""
<html>
    <head>
        {% if title %}
        <title>{{ title }} - Microblog</title>
        {% else %}
        <title>Welcome to Microblog!</title>
        {% endif %}
    </head>
    <body>
        <h1>Hello, {{ user.username }}!</h1>
    </body>
</html>
"""