# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:39:03 2020

@author: Owen
"""

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, OrderForm
from app.models import Users, Suppliers, Orders, InventoryInOrder, InventoryItems
from app.place_order import send_order, read_response
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
    inv_for_display = InventoryItems.query.all() # inefficient
    if current_user.supplier_id: # if they are a supplier, they should only see their own products
        inv_for_display = InventoryItems.query.filter_by(supplier_id=current_user.supplier_id).all()
    else: # otherwise, check for a delivery confirmation
        responses = read_response() #dictionary of emails
        refresh = False
        if responses:
            for order_id in responses:
                order = Orders.query.filter_by(id=order_id).first()
                if order.is_confirmed or order.is_confirmed == False: # unconfirmed/undenined orders are None
                    continue # this order has already been confirmed or declined and the db updated. The email has not been deleted yet. Ignore it
                if responses[order_id]: # if the order was confirmed
                    order.is_confirmed = True
                    db.session.add(order)
                    db.session.commit()
                    ####### Update the inventory quantities ########
                    order_inventory = InventoryInOrder.query.filter_by(order_id=order_id).all()
                    for ordered_inv in order_inventory:
                        ordered_inv.inventory.SKUs += ordered_inv.SKUs
                        db.session.add(ordered_inv.inventory)
                        db.session.commit()
                    flash("Note: Order number {} was confirmed. Expected delivery date of {}. The database has been updated."\
                          .format(order_id, order.order_ETA))
                    refresh = True
                else:
                    order.is_confirmed = False
                    db.session.add(order)
                    db.session.commit()
                    flash("Note: Order number {} was declined".format(order_id))
                    refresh = True
                    
            if refresh:
                return redirect(url_for('index')) # refresh the page to show the user the flashed messages
            
    for inventory in inv_for_display:
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
    # TODO: add in the functionally determined optimal order quantity and Re-order point
    # TODO: create buttons that allow inventory to be sorted (for status that will be WIP vs. complete)
    # TODO: allow inventory to be modified on the homepage for admins
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
        send_order(order.id)
        flash('Placed an order for {} SKUs of {}. Pending supplier confirmation.'.format(inv_in_order.SKUs, product.item_name))
        return redirect(url_for('index'))
    ################################
    
    return render_template('index.html', title='Home', inventories=inventories, form=form)


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
