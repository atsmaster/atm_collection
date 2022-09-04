from peewee import CompositeKey, IntegerField, CharField, Database, TextField, FixedCharField, DecimalField, DoubleField, FloatField, TimestampField

from client.model.BaseModel import BaseModel


class CoinEntry(BaseModel):
    class Meta:
        db_table = 'coin_entry'
        primary_key = CompositeKey('exchange', 'symbol')

    exchange = CharField()
    symbol = CharField()
    status = CharField()
    base_asset = CharField()
    quote_asset = CharField()
    base_asset_precision = IntegerField()
    quote_asset_precision = IntegerField()
    onboard_date = TimestampField()

    deci = DecimalField()
