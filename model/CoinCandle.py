from peewee import CompositeKey, CharField, DoubleField, FixedCharField

from model.BaseModel import BaseModel


class CoinCandle(BaseModel):

    class Meta:
        primary_key = CompositeKey('symbol', 'open_time')

    symbol = CharField(64)
    # open_time = DateTimeField()
    open_time = FixedCharField(8)
    open = DoubleField()
    close = DoubleField()
    high = DoubleField()
    low = DoubleField()

