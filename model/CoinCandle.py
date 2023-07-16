from peewee import CompositeKey, CharField, DoubleField, FixedCharField, DateTimeField

from model.BaseModel import BaseModel


class CoinCandle(BaseModel):

    class Meta:
        primary_key = CompositeKey('symbol', 'open_dttm')

    symbol = CharField(64, column_name='SYMBOL')
    # open_time = DateTimeField()
    open_dttm = DateTimeField(8, column_name='OPEN_DTTM')
    open = DoubleField(column_name='OPEN')
    close = DoubleField(column_name='CLOSE')
    high = DoubleField(column_name='HIGH')
    low = DoubleField(column_name='LOW')

