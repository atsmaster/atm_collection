from peewee import CompositeKey, CharField, DoubleField, FixedCharField

from model.BaseModel import BaseModel


class CoinCandle(BaseModel):

    class Meta:
        primary_key = CompositeKey('symbol', 'open_time')

    symbol = CharField(64, column_name='SYMBOL')
    # open_time = DateTimeField()
    open_time = FixedCharField(8, column_name='OPEN_TIME')
    open = DoubleField(column_name='OPEN')
    close = DoubleField(column_name='CLOSE')
    high = DoubleField(column_name='HIGH')
    low = DoubleField(column_name='LOW')

