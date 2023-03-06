import configparser
import datetime

from peewee import Model, DateTimeField

from config.DatabaseConfig import Database


class BaseModel(Model):

    class Meta:
        database = Database().conn()

