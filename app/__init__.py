# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:34:05 2020

@author: Owen
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this-password-is-next-level'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:q1w2e3@localhost:5432/Inventory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
db.create_all()

from app import routes, models