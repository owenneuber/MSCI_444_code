# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:06:55 2020

@author: Owen
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField
from wtforms.validators import DataRequired, ValidationError
from app.models import InventoryItems

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