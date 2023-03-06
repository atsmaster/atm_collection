from client.model.CoinCandleBinanceMin import CoinCandleBinanceMin
from client.model.CoinCandleFactory import CoinCandleFactory
import datetime as dt
import peewee
from com.ComDate import ComDate

class Backtest:

    def __int__(self, exchange):
        self.coin_candle = CoinCandleBinanceMin


