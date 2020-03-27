# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:55:31 2020

@author: Owen
"""

from numpy import sqrt
import speech_recognition as srg

def EOQ(ordering_cost, holding_cost,demand):
    return int(sqrt(2*ordering_cost*demand/holding_cost))

def reorder_point(lead_time, demand):
    return int(demand/30*lead_time) # divide demand by 30 to convert monthly to daily

def voice_order():
    rec = srg.Recognizer()
    with srg.Microphone() as source:
        print("Say something. ")
        paudio = rec.listen(source)
        print("Finished! ")
        
        # determine product output
        org=rec.recognize_google(paudio)
        output= rec.recognize_google(paudio)
        print(output)
        # expected format of "place an order for 50 steel beams"
        output = output.strip().split("for")
        if output[0].strip() != "place an order": # if format not followed
            return False, org
        SKUs = int(output[1].strip().split(" ")[0])
        product_name = output[1].strip().replace(str(SKUs),"").strip()
        
        # capitalize the name
        product_name = " ".join([word.capitalize() for word in product_name.split(" ")])

        return product_name, SKUs