import configparser
import datetime

from peewee import Model, DateTimeField

from db.Database import Database


class BaseModel(Model):

    class Meta:
        database = Database().conn()

