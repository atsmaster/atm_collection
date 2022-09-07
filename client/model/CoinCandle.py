from peewee import CompositeKey, CharField, DoubleField, DateTimeField

from client.model.BaseModel import BaseModel


class CoinCandle(BaseModel):

    class Meta:
        # db_table = 'coin_entry'
        primary_key = CompositeKey('symbol', 'time_interval', 'open_time')

    symbol = CharField()
    time_interval = CharField()
    open_time = DateTimeField()
    open = DoubleField()
    close = DoubleField()
    high = DoubleField()
    low = DoubleField()

