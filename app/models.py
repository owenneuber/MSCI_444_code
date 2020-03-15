from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, db # if this does not work, change modelds' directory into /app

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Users(UserMixin, db.Model): #user Table
    __tablename__ = 'Users'
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String, unique=True, index=True)
    user_type = db.Column(db.String) # admin, supplier, or view-only
    password_hash = db.Column(db.String)
    
    supplier_id = db.Column(db.Integer, db.ForeignKey("Suppliers.id"))
    supplier = db.relationship('Suppliers', foreign_keys=[supplier_id])
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Users(UserID='{}', UserName='{}', UserType={}, SupplierID={})>"\
                .format(self.id, self.user_name, self.user_type, self.supplier_id)
 
class Suppliers(db.Model): #Supplier Table
    __tablename__ = 'Suppliers'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    supplier_type = db.Column(db.String) # primary or secondary
    email = db.Column(db.String, unique=True, index=True)
    location = db.Column(db.String)
    phone_number = db.Column(db.String, unique=True, index=True) # (777) 777-7777 format
    order_format = db.Column(db.String)

    def __repr__(self):
        return "<Users(SupplierID='{}', SupplierType='{}', Email={}, Location={}, PhoneNumber={}, OrderFormat={})>"\
                .format(self.id, self.supplier_type, self.email, self.location,self.phone_number,self.order_format)

class Orders(db.Model): #Orders Table
    __tablename__ = 'Orders'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    supplier_id = db.Column(db.Integer, db.ForeignKey("Suppliers.id"))
    order_placed = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    order_ETA = db.Column(db.Date)
    
    supplier = db.relationship('Suppliers', foreign_keys=[supplier_id])
    user = db.relationship('Users', foreign_keys=[user_id])

    def __repr__(self):
        return "<Users(OrderID='{}',OrderPlaced='{}', UserID={}, SupplierID={}, Order_ETA={}))>"\
                .format(self.id, self.order_placed, self.user_id, self.supplier_id,self.order_ETA)

class InventoryInOrder(db.Model): #table for Inventory in order
    __tablename__ = 'InventoryInOrder'
    id = db.Column(db.Integer,primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("Orders.id"))
    SKUs = db.Column(db.Integer)
    inventory_id = db.Column(db.Integer, db.ForeignKey("InventoryItems.id"))
    
    order = db.relationship('Orders', foreign_keys=[order_id])
    inventory = db.relationship('InventoryItems', foreign_keys=[inventory_id])

    def __repr__(self):
        return "<Users(ID='{}', OrderID='{}', SKUs='{}', InventoryID={})>"\
                .format(self.id, self.order_id, self.SKUs, self.inventory_id)

class InventoryItems(db.Model): #table for Inventory in order
    __tablename__ = 'InventoryItems'
    id = db.Column(db.Integer,primary_key = True)
    item_name = db.Column(db.String)
    inventory_type = db.Column(db.String) # complete, WIP
    supplier_id = db.Column(db.Integer, db.ForeignKey("Suppliers.id"))
    lead_time = db.Column(db.Integer) # maybe db.DateTime for adding days
    SKUs = db.Column(db.Integer)
    ordering_cost = db.Column(db.Float)
    holding_cost = db.Column(db.Float)
    variable_cost = db.Column(db.Float)
    demand = db.Column(db.Integer) # days
    
    supplier = db.relationship('Suppliers', foreign_keys=[supplier_id])
    
    def __repr__(self):
        return "<Users(ItemName='{}', SKUs='{}', InventoryID={}, InventoryType={},SupplierID={}, LeadTime={}, OrderingCost={}, HoldingCost={}, VariableCost={}, Demand={}>"\
                .format(self.item_name, self.SKUs, self.id,self.inventory_type,self.supplier_id,self.lead_time,self.ordering_cost,self.holding_cost,self.variable_cost,self.demand) 