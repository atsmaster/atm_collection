import datetime as dt
from peewee import CompositeKey, IntegerField, CharField
from model.BaseModel import BaseModel


class CoinEntry(BaseModel):

    class Meta:
        db_table = 'TB_COIN_ENTRY'
        primary_key = CompositeKey('exchange', 'symbol')

    exchange = CharField(column_name='EXCHANGE')
    symbol = CharField(column_name='SYMBOL')
    symbol_status_cd = CharField(column_name='SYMBOL_STATUS_CD')
    base_asset = CharField(column_name='BASE_ASSET')
    quote_asset = CharField(column_name='QUOTE_ASSET')
    base_asset_precision = IntegerField(column_name='BASE_ASSET_PRECISION')
    quote_asset_precision = IntegerField(column_name='QUOTE_ASSET_PRECISION')
    onboard_date = CharField(12, column_name='ONBOARD_DATE')

    def convert_onboard_date_to_datetime(self):
        self.onboard_date = dt.datetime.strptime(self.onboard_date, '%Y%m%d%H%M')

    def __eq__(self, other):
        # if self.exchange != other.exchange:
        #     return False
        if self.symbol != other.symbol:
            return False
        if self.symbol_status_cd != other.symbol_status_cd:
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




