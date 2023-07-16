from peewee import FixedCharField, BooleanField, CharField, IntegerField, PrimaryKeyField, DateTimeField

from model.BaseModel import BaseModel


class CoinEntryHist(BaseModel):
    class Meta:
        db_table = 'TB_COIN_ENTRY_HIST'
        # primary_key
        indexes = (
            (('exchange', 'symbol'), False),
        )

    seq = PrimaryKeyField(column_name='SEQ')
    exchange = CharField(column_name='EXCHANGE')
    symbol = CharField(column_name='SYMBOL')
    symbol_status_cd = CharField(column_name='SYMBOL_STATUS_CD')
    base_asset = CharField(column_name='BASE_ASSET')
    quote_asset = CharField(column_name='QUOTE_ASSET')
    base_asset_precision = IntegerField(column_name='BASE_ASSET_PRECISION')
    quote_asset_precision = IntegerField(column_name='QUOTE_ASSET_PRECISION')
    onboard_dttm = DateTimeField(12, column_name='ONBOARD_DTTM')
    list_cd = FixedCharField(max_length=1, column_name='LIST_CD')  # N : 신규 상장, D : 상장 폐지, R : 재상장, L : 기존 종목 정보 변경
    price_use_yn = BooleanField(column_name='PRICE_USE_YN')
    # create_date = DateTimeField(default=datetime.datetime.now())
