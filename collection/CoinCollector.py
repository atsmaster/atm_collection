from abc import *


class CoinCollector(metaclass=ABCMeta):

    @abstractmethod
    def get_coin_info(self):
        pass

    @abstractmethod
    def get_coin_candle(self):
        pass
