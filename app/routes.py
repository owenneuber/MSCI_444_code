# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:39:03 2020

@author: Owen
"""

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
from app.models import Users, Suppliers, Orders, InventoryInOrder, InventoryItems
from flask_login import current_user, login_user, logout_user, login_required
# from sqlalchemy.orm import sessionmaker
from werkzeug.urls import url_parse
#engine = create_engine(DATABASE_URI)
#session = Session()

@app.route('/')
@app.route('/index')
@login_required
def index():
    """
    posts = [
        {
            'author': {'user_name': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'user_name': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    """
    
    inventories = []
    for inventory in InventoryItems.query.all():
        inventories.append({
                'id':inventory.id,
                'item_name':inventory.item_name,
                'inventory_type':inventory.inventory_type,
                'supplier':inventory.supplier.name,
                'SKUs':inventory.SKUs,
                'lead_time':inventory.lead_time,
                'ordering_cost':inventory.ordering_cost,
                'holding_cost':inventory.holding_cost,
                'variable_cost':inventory.variable_cost,
                'demand':inventory.demand,
                })
    # TODO: add in the functionally determined stuff like reorder point        
    
    return render_template('index.html', title='Home', inventories=inventories)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(user_name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

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