from client.binance.future.BnFutureReqClient import BnFutureReqClient
from client.enum.ExchangeEnum import ExchangeEnum


class ReqClientFactory:

    @classmethod
    def create_req(cls, exchange_enum):
        if exchange_enum == ExchangeEnum.BINANCE.value:
            return BnFutureReqClient()
        else:
            return None
