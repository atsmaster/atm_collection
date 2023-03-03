from peewee import CompositeKey

from client.model.BaseModel import BaseModel
from client.model.CoinCandle import CoinCandle


class CoinCandleBinanceMin(CoinCandle):

    class Meta:
        db_table = 'coin_candle_binance_min'


