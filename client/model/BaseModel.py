import configparser
from peewee import Model

from db.Database import Database


class BaseModel(Model):

    class Meta:
        database = Database().conn()
