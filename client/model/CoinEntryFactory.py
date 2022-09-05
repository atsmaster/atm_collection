from client.enum.ExchangeEnum import ExchangeEnum
from client.model.CoinEntryBinance import CoinEntryBinance


class CoinEntryFactory:
    @classmethod
    def create_entry(cls, exchange_enum):
        if exchange_enum == ExchangeEnum.BINANCE.value:
            return CoinEntryBinance
        else:
            return None
