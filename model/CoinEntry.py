import datetime
import datetime as dt
from peewee import CompositeKey, IntegerField, CharField, DateTimeField
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
    onboard_dttm = DateTimeField(column_name='ONBOARD_DTTM')
    createdDttm = DateTimeField(column_name='CREATED_DTTM', default=datetime.datetime.now())
    modifiedDttm = DateTimeField(column_name='MODIFIED_DTTM', default=None)


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
        if self.onboard_dttm != other.onboard_dttm:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)




