# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:06:55 2020

@author: Owen
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField
from wtforms.validators import DataRequired, ValidationError, Optional
from app.models import InventoryItems, Suppliers

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class OrderForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()], render_kw={"placeholder": "Product ID"})
    quantity = IntegerField("Order Quantity", validators=[DataRequired()], render_kw={"placeholder": "# of SKUs"})
    submit = SubmitField('Place Order')
    
    def validate_product_id(self, product_id):
        product = InventoryItems.query.filter_by(id=product_id.data).first()
        if product is None:
            raise ValidationError("Choose an existing product ID.")
            
class ModifyInventoryForm(FlaskForm):
    product_mod_id = IntegerField('Product Mod ID', validators=[DataRequired()], render_kw={"placeholder": "Product ID"})
    name = StringField("New Name", validators=[Optional()], render_kw={"placeholder": "New Name"})
    prod_type = StringField("Type", validators=[Optional()], render_kw={"placeholder": "Type"})
    supplier = StringField("Supplier", validators=[Optional()], render_kw={"placeholder": "Supplier"})
    SKUs = IntegerField("SKUs", validators=[Optional()], render_kw={"placeholder": "SKUs"})
    lead_time = IntegerField("Lead Time", validators=[Optional()], render_kw={"placeholder": "Lead Time"})
    ordering_cost = IntegerField("Ordering Cost", validators=[Optional()], render_kw={"placeholder": "Ordering Cost"})
    holding_cost = IntegerField("Holding Cost", validators=[Optional()], render_kw={"placeholder": "Holding Cost"})
    variable_cost = IntegerField("Variable Cost", validators=[Optional()], render_kw={"placeholder": "Variable Cost"})
    demand = IntegerField("Demand", validators=[Optional()], render_kw={"placeholder": "Demand"})
    submit = SubmitField('Update Fileds')
    
    def validate_product_mod_id(self, product_mod_id):
        product = InventoryItems.query.filter_by(id=product_mod_id.data).first()
        if product is None:
            raise ValidationError("Choose an existing product ID.")
            
    def validate_prod_type(self, prod_type):
        prod_type = prod_type.data
        if prod_type is None or prod_type == "": # bad form but the one-liner was not working for some reason
            pass
        elif prod_type=="WIP":
            pass
        elif prod_type=="Complete":
            pass
        else:
            raise ValidationError("Product Type must be either 'Complete' or 'WIP'.")
            
    def validate_supplier(self, supplier):
        if supplier.data is None or supplier.data == "":
            pass
        else:
            supplier_instance = Suppliers.query.filter_by(name=supplier.data).first()
            if not supplier_instance: #they picked a supplier not in our records
                raise ValidationError("Selected supplier must be an existing supplier.")
                
class VoiceOrderForm(FlaskForm):
    submit = SubmitField('Place Order')