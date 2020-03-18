# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 19:42:51 2020

@author: Owen
"""

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.models import Orders, Users, Suppliers, InventoryInOrder, InventoryItems
import imaplib

def send_order(order_id):
    """ Take in the order_id integer and then accesses the database to extract
    the details of the order. Then sends the relevant email to the supplier. """
    
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "msci444ims@gmail.com"  # Enter your address
    password = "Let'sgo!"
    
    supplier = Orders.query.filter_by(id=order_id).first().supplier
    receiver_email = supplier.email
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Order ID: {}".format(str(order_id))
    message["From"] = sender_email
    message["To"] = receiver_email
    text_backup = "To {},\n\n We would like to place the following order:\n".format(supplier.name)
    html = "To {},<br><br>We would like to place the following order:<br><br>".format(supplier.name)
    
    html_table_core = supplier.order_format.split("<div>")[1].split("</div>")[0]
    html+= supplier.order_format.split("<div>")[0]
    
    text_table_core = html_table_core.replace("</td><td>",",\t").replace("<td>","").replace("</td>","").replace("<tr>","").replace("</tr>","\n")
    text_backup+= supplier.order_format.split("<tr>")[1].split("</tr>")[0].replace("</td><td>",",\t").replace("<td>","").replace("</td>","").replace("<tr>","").replace("</tr>","\n")
    
    inv_in_order = InventoryInOrder.query.filter_by(order_id=order_id).all() # list of all inventory in the specific order
    for order_inv in inv_in_order:
        html+= html_table_core.format(inventory_id=order_inv.inventory.id, item_name=order_inv.inventory.item_name, SKUs=order_inv.SKUs, variable_cost=order_inv.inventory.variable_cost)
        text_backup+= text_table_core.format(inventory_id=order_inv.inventory.id, item_name=order_inv.inventory.item_name, SKUs=order_inv.SKUs, variable_cost=order_inv.inventory.variable_cost)
    html+= supplier.order_format.split("</div>")[1] # add in that </table> or anything else
    
    html += '''
    <br>
    Thanks,<br><br>
    Owen Neuber<br>
    Inventory Manager<br>
    msci444ims@gmail.com'''
    text_backup += '''
    Thanks,
    Owen Neuber
    Inventory Manager
    msci444ims@gmail.com'''
    part1 = MIMEText(text_backup, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, str(message)
        )

def read_response():
    """ This function should be triggered each time the /index page refreshes.
    It will check for any order confirmations or declines. Its output is either
    False if no emails have been received since the last check, or it will return
    a dictionary of the format {{order_id:True},{order_id:Flase},...} where True
    corresponds to a confirmed order and False corresponds to a declined order. """
    
    # see https://codehandbook.org/how-to-read-email-from-gmail-using-python/ for code
    
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    email = "msci444ims@gmail.com"  # Enter your address
    password = "Let'sgo!"
    
    mail = imaplib.IMAP4_SSL(smtp_server)
    mail.login(email,password)
    
    mail.select('inbox')
    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])


if __name__ == "__main__":
    pass