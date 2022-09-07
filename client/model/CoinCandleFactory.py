from client.enum.ExchangeEnum import ExchangeEnum
from client.model.CoinCandleBinance import CoinCandleBinance


class CoinCandleFactory:
    @classmethod
    def create_entry(cls, exchange_enum):
        if exchange_enum == ExchangeEnum.BINANCE.value:
            return CoinCandleBinance
        else:
            return None
