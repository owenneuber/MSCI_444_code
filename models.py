from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()
DATABASE_URI = 'postgres+psycopg2://postgres:q1w2e3@localhost:5432/Inventory'

class Users(Base): #user Table
    __tablename__ = 'Users'
    id = Column(Integer,primary_key=True)
    user_name = Column(String)
    user_type = Column(String) # admin, supplier, or view-only
    
    supplier_id = Column(Integer, ForeignKey("Suppliers.id"))
    supplier = relationship('Suppliers', foreign_keys=[supplier_id])

    def __repr__(self):
        return "<Users(UserID='{}', UserName='{}', UserType={}, SupplierID={})>"\
                .format(self.id, self.user_name, self.user_type, self.supplier_id)
 
class Suppliers(Base): #Supplier Table
    __tablename__ = 'Suppliers'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    supplier_type = Column(String) # primary or secondary
    email = Column(String)
    location = Column(String)
    phone_number = Column(String) # (777) 777-7777 format
    order_format = Column(String)

    def __repr__(self):
        return "<Users(SupplierID='{}', SupplierType='{}', Email={}, Location={}, PhoneNumber={}, OrderFormat={})>"\
                .format(self.id, self.supplier_type, self.email, self.location,self.phone_number,self.order_format)

class Orders(Base): #Orders Table
    __tablename__ = 'Orders'
    id = Column(Integer,primary_key=True)
    time_stamp = Column(String)
    user_id = Column(Integer, ForeignKey("Users.id"))
    supplier_id = Column(Integer, ForeignKey("Suppliers.id"))
    order_ETA = Column(Date)
    
    supplier = relationship('Suppliers', foreign_keys=[supplier_id])
    user = relationship('Users', foreign_keys=[user_id])

    def __repr__(self):
        return "<Users(OrderID='{}',TimeStamp='{}', UserID={}, SupplierID={}, Order_ETA={}))>"\
                .format(self.id, self.time_stamp, self.user_id, self.supplier_id,self.order_ETA)

class InventoryInOrder(Base): #table for Inventory in order
    __tablename__ = 'InventoryInOrder'
    id = Column(Integer,primary_key=True)
    order_id = Column(Integer, ForeignKey("Orders.id"))
    SKUs = Column(Integer)
    inventory_id = Column(Integer, ForeignKey("InventoryItems.id"))
    
    order = relationship('Orders', foreign_keys=[order_id])
    inventory = relationship('InventoryItems', foreign_keys=[inventory_id])

    def __repr__(self):
        return "<Users(ID='{}', OrderID='{}', SKUs='{}', InventoryID={})>"\
                .format(self.id, self.order_id, self.SKUs, self.inventory_id)

class InventoryItems(Base): #table for Inventory in order
    __tablename__ = 'InventoryItems'
    id = Column(Integer,primary_key = True)
    item_name = Column(String)
    inventory_type = Column(String) # complete, WIP
    supplier_id = Column(Integer, ForeignKey("Suppliers.id"))
    lead_time = Column(Integer) # maybe datetime for adding days
    SKUs = Column(Integer)
    ordering_cost = Column(Float)
    holding_cost = Column(Float)
    variable_cost = Column(Float)
    demand = Column(Integer) # days
    
    supplier = relationship('Suppliers', foreign_keys=[supplier_id])
    
    def __repr__(self):
        return "<Users(ItemName='{}', SKUs='{}', InventoryID={}, ItemName={}), InventoryType={},SupplierID={}, LeadTime={}, OrderingCost={}, HoldingCost={}, VariableCost={}, Demand={}>"\
                .format(self.item_name, self.SKUs, self.id,self.item_name,self.inventory_type,self.lead_time,self.ordering_cost,self.holding_cost,self.variable_cost,self.demand) 