# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:34:05 2020

@author: Owen
"""

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this-password-is-next-level'

from app import routes