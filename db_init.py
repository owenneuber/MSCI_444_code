# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 14:46:13 2020

@author: Owen

Run this to fill your empty database with tables
"""

from app import db

db.create_all() #uncomment this line when running to initialize the database

""" jenny's password is cats
u = Users(user_name="owen",user_type="admin")
u.set_password('dank')
db.session.add(u)
db.session.commit()

sup = Suppliers(name="jenny",supplier_type="primary",email="jenny@gmail.com",location="Main",phone_number="(888) 867-5309",order_format="<HTML>Stuff<\HTML>")
steel = InventoryItems(item_name="Steel beams", inventory_type="complete",supplier_id=1,lead_time=5,SKUs=5000,ordering_cost=50,holding_cost=10,variable_cost=5,demand=100)


Users.query.filter_by(user_name="owen").first() # format for a query

"""