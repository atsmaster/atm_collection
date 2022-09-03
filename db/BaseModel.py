import configparser
from peewee import Model, mysql

properties = configparser.ConfigParser()
properties.read('C:/atm_collection_master/config.ini')
database = properties["DATABASE"]
db = database["DB"]
host = database["HOST"]
port = int(database["PORT"])
user = database["USER"]
password = database["PASSWORD"]

conn = mysql.connect(host=host, port=port, user=user, password=password, db=db)

class BaseModel(Model):
    class Database:
        database = conn

