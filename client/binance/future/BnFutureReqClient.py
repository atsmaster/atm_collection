from binance_f import RequestClient
from binance_f.constant.test import *
from client.ReqClient import ReqClient
from client.model.Entry import *


class BnFutureReqClient(ReqClient):

    def __init__(self):
        with open("C:/atm_collection_master/config.txt") as f:
            lines = f.readlines()
            api_key = lines[0].strip()
            secret = lines[1].strip()
        self.request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

    def get_coin_info(self):
        aa = self.request_client.get_exchange_information()
        print(aa.symbols[0].baseAsset)
        # Entry(aa.)
        return "a"

    def get_coin_candle(self):
        pass


aab = BnFutureReqClient().get_coin_info()