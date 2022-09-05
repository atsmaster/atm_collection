from abc import *


class ReqClient(metaclass=ABCMeta):

    @abstractmethod
    def get_entry(self):
        pass

    @abstractmethod
    def get_candle(self):
        pass