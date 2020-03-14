#run this file to create/destrop tables
from sqlalchemy import create_engine
from models import *

def recreate_database(): # destroyes and recreates the tables in the database
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

engine = create_engine(DATABASE_URI)
recreate_database()


