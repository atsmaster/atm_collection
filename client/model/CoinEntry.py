import sys
from peewee import CompositeKey, IntegerField, CharField
import peewee

from db.BaseModel import BaseModel


class CoinEntry(BaseModel):
    class Meta:
        db_table = "CoinEntry"
        primary_key = CompositeKey('aaa', 'bbb')

    aaa = IntegerField()
    bbb = IntegerField()
    ccc = CharField()


class CoinEntry2(BaseModel):
    class Meta:
        db_table = "CoinEntry"
        primary_key = CompositeKey('aaa', 'bbb')

    aaa = IntegerField()
    bbb = IntegerField()
    ccc = CharField()


aa = CoinEntry.create()

ab = 0