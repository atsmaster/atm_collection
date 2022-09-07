from peewee import CompositeKey, IntegerField, CharField, DateTimeField

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
    onboard_date = DateTimeField()

    def __eq__(self, other):
        # if self.exchange != other.exchange:
        #     return False
        if self.symbol != other.symbol:
            return False
        if self.status != other.status:
            return False
        if self.base_asset != other.base_asset:
            return False
        if self.quote_asset != other.quote_asset:
            return False
        if self.base_asset_precision != other.base_asset_precision:
            return False
        if self.quote_asset_precision != other.quote_asset_precision:
            return False
        if self.onboard_date != other.onboard_date:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)




