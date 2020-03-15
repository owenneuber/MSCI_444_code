# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:39:03 2020

@author: Owen
"""

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, OrderForm
from app.models import Users, Suppliers, Orders, InventoryInOrder, InventoryItems
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime, timedelta
# from sqlalchemy.orm import sessionmaker
from werkzeug.urls import url_parse
#engine = create_engine(DATABASE_URI)
#session = Session()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    ########## Display Table ############
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
    # TODO: add in the functionally determined stuff like reorder point and order quantity
    # TODO: Send emails and parse the outputs
    # TODO: change what supplier and view-only users see.
    ############ Place an Order ################
    form = OrderForm()
    if form.validate_on_submit():
        product = InventoryItems.query.filter_by(id=form.product_id.data).first()
        order = Orders(user_id=current_user.id, supplier_id=product.supplier_id, order_ETA=datetime.utcnow().date() + timedelta(days=product.lead_time))
        db.session.add(order)
        db.session.commit()
        inv_in_order = InventoryInOrder(order_id=order.id, SKUs=form.quantity.data, inventory_id=product.id)
        db.session.add(inv_in_order)
        db.session.commit()
        flash('Placed an order for {} SKUs of {}. Pending supplier confirmation.'.format(inv_in_order.SKUs, product.item_name))
        return redirect(url_for('index'))
    
    
    return render_template('index.html', title='Home', inventories=inventories, form=form)

"""
class OrderForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    quantity = IntegerField("Order Quantity", validators=[DataRequired()])
    submit = SubmitField('Place Order')
    
    def validate_order(self, product_id):
        product = InventoryItems.query.filter_by(id=product_id.data).first()
        if product is None:
            raise ValidationError("Choose an existing product ID.")
            """


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