import configparser
from peewee import MySQLDatabase


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):
    connection = None

    def conn(self):
        if self.connection is None:
            properties = configparser.ConfigParser()
            properties.read('D:/atm_master/config.ini')
            database = properties["DATABASE"]
            db = database["DB"]
            host = database["HOST"]
            port = int(database["PORT"])
            user = database["USER"]
            password = database["PASSWORD"]
            self.connection = MySQLDatabase(db, host=host, port=port, user=user, password=password)
        return self.connection
