# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:54:22 2020

@author: Owen

Run this script to populate the database
"""

from app import db
from app.models import Users, Suppliers, InventoryItems

"""
add users as follows:
u = Users(user_name="owen",user_type="admin") # can set supplier_id here to link to a supplier
u.set_password('dank')
db.session.add(u)
db.session.commit()
"""

def get_supplier_id(supplier_name):
    return Suppliers.query.filter_by(name=supplier_name).first().id

#### Add Suppliers ####
""" uncomment if you would like to add the suppliers
# all order formats the same for demo purposes
order_format = '''<table border="1">
<tr>
<td>Inventory ID</td><td>Inventory Name</td><td>SKUs Ordered</td><td>Cost/SKU</td>
</tr>
<tr>
<div><td>{inventory_id}</td><td>{item_name}</td><td>{SKUs}</td><td>${variable_cost}</td>
</tr></div>
</table>'''
email = "owenneuber@outlook.com" # all set to me for demo purposes
location = "Waterloo" # all set the same for demo
supplier_type = "primary" # all set the same for demo purposes
phone_number_base = "(777) 777-777"
supplier_names = ["Home Depot", "Metals Depot", "Global Industrial", "Staples", "RONA"]

counter = 0
for supplier_name in supplier_names:
    counter+=1
    sup = Suppliers(name=supplier_name,supplier_type=supplier_type,email=email,location=location,phone_number=phone_number_base+str(counter),order_format=order_format)
    db.session.add(sup)
    db.session.commit()
    
# Add Home Depot as a Supplier User
u = Users(user_name="home_depot",user_type="supplier", supplier_id=get_supplier_id("Home Depot")) # make home depo a supplier user
u.set_password('dank')
db.session.add(u)
db.session.commit()
"""

#### Add Inventory ####
inventory_rows = open("s_inventory_rows.csv","r")
for row in inventory_rows:
    data = row.strip().split(",")
    data = [x.strip(' ') for x in data] # remove any trailing or leading spaces
    inv = InventoryItems(item_name=data[1], inventory_type=data[2],supplier_id=get_supplier_id(data[3]),SKUs=int(data[4]),lead_time=int(data[5]),ordering_cost=float(data[6]),holding_cost=float(data[7]),variable_cost=float(data[8]),demand=int(data[9]))
    db.session.add(inv)
    db.session.commit()
    
inventory_rows.close()