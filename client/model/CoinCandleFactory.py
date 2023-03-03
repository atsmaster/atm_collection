from client.enum.ExchangeEnum import ExchangeEnum
from client.model.CoinCandleBinanceMin import CoinCandleBinanceMin


class CoinCandleFactory:
    @classmethod
    def create_entry(cls, exchange_enum):
        if exchange_enum == ExchangeEnum.BINANCE.value:
            return CoinCandleBinanceMin
        else:
            return None
