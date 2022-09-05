from peewee import CompositeKey, FixedCharField, BooleanField, CharField

from client.model.BaseModel import BaseModel


class CoinEntryStatus(BaseModel):
    class Meta:
        db_table = 'coin_entry_status'
        primary_key = CompositeKey('exchange', 'symbol')

    exchange = CharField()
    symbol = CharField()
    list_cd = FixedCharField(max_length=1)  # N : 신규 상장, L : 상장중, D 상장 폐지
    price_use_yn = BooleanField()
