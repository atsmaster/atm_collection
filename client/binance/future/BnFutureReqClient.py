import configparser

from binance.um_futures import UMFutures
from client.ReqClient import ReqClient
from client.model.CoinEntry import *


class BnFutureReqClient(ReqClient):

    def __init__(self):
        properties = configparser.ConfigParser()
        properties.read('C:/atm_collection_master/config.ini')
        database = properties["BN"]
        api_key = database["API_KEY"]
        secret_key = database["SEC_KEY"]
        self.um_futures_client = UMFutures(key=api_key, secret=secret_key)

    def get_coin_info(self):
        coin_entry_list = []
        for e in self.um_futures_client.exchange_info()['symbols']:
            c = CoinEntry.create(
                exchange='BN',
                symbol=e['symbol'],
                status=e['status'],
                base_asset=e['baseAsset'],
                quote_asset=e['quoteAsset'],
                base_asset_precision=e['baseAssetPrecision'],
                quote_asset_precision=e['pricePrecision'],
                onboard_date=e['onboardDate']
            )
            coin_entry_list.append(c)
        return coin_entry_list

    def get_coin_candle(self):
        pass

    def get_account(self):
        aaabb = self.um_futures_client.account(recvWindow=6000)
        return 0


aab = BnFutureReqClient().get_coin_info()
iab = 0
