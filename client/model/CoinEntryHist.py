import datetime

from peewee import CompositeKey, FixedCharField, BooleanField, CharField, IntegerField, DateTimeField, PrimaryKeyField

from client.model.BaseModel import BaseModel


class CoinEntryHist(BaseModel):
    class Meta:
        db_table = 'coin_entry_hist'
        # primary_key
        indexes = (
            (('exchange', 'symbol'), False),
        )

    seq = PrimaryKeyField()
    exchange = CharField()
    symbol = CharField()
    status = CharField()
    base_asset = CharField()
    quote_asset = CharField()
    base_asset_precision = IntegerField()
    quote_asset_precision = IntegerField()
    onboard_date = DateTimeField()
    list_cd = FixedCharField(max_length=1)  # N : 신규 상장, D : 상장 폐지, R : 재상장, L : 기존 종목 정보 변경
    price_use_yn = BooleanField()
    # create_date = DateTimeField(default=datetime.datetime.now())
