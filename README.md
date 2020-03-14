# MSCI_444_code


## Installing Database

1. [Install Python](https://medium.com/bb-tutorials-and-thoughts/how-to-install-and-getting-started-with-python-acf369e4cf80)
2. [Install PostgreSQL](https://www.postgresql.org/download/) (set your postgres password to "q1w2e3")
3. [Install Git](https://gitforwindows.org/)
4. [Clone this repository](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)
5. Create an empty database named "Inventory" in pgAdmin
6. Run initialize_db.py

The database should now be created and it should have all of its tables formatted

### Populating the database

In a python session, (in the same directory as your downloaded files) run the following:

```
from sqlalchemy.orm import sessionmaker
engine = create_engine(DATABASE_URI)
session = Session()
```

Then to add users, do the following:
```
user = Users(user_name="owen",user_type="admin")
session.add(user)
session.commit()
```

Likewise, you can add other DB information like suppliers and inventory:
```
sup = Suppliers(supplier_type="primary",email="jenny@gmail.com",location="Main",phone_number="(888) 867-5309",order_format="<HTML>Stuff<\HTML>")
steel = InventoryItems(item_name="Steel beams", inventory_type="complete",supplier_id=1,lead_time=5,SKUs=5000,ordering_cost=50,holding_cost=10,variable_cost=5,demand=100)
session.add(steel)
session.add(sup)
session.commit()
```

If you ever cause errors, run:
```
session.rollback()
```
and that should clean things up.

Feel free to add as many rows as you'd like to any tables.

When you are done adding stuff, always ALWAYS end your session with:
```
session.close()
```

## Problems

If you get an error saying you don't have a specific package just type into the Windows Command Processor:
```
pip install <package-name>
```
That should install your missing package. Keep doing this forr each package you need to install.