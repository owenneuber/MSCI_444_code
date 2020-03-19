# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:55:31 2020

@author: Owen
"""

from numpy import sqrt

def EOQ(ordering_cost, holding_cost,demand):
    return int(sqrt(2*ordering_cost*demand/holding_cost))

def reorder_point(lead_time, demand):
    return int(demand/30*lead_time) # divide demand by 30 to convert monthly to daily

