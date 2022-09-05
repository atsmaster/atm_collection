from peewee import CompositeKey, IntegerField, CharField, TimestampField, BooleanField

from client.model.BaseModel import BaseModel


class CoinEntry(BaseModel):
    class Meta:
        # db_table = 'coin_entry'
        primary_key = CompositeKey('symbol')

    symbol = CharField()
    status = CharField()
    base_asset = CharField()
    quote_asset = CharField()
    base_asset_precision = IntegerField()
    quote_asset_precision = IntegerField()
    onboard_date = TimestampField()
    is_listed = BooleanField()

