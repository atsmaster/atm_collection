import configparser

from binance.um_futures import UMFutures
from client.ReqClient import ReqClient
from client.model.CoinEntry import *


class BnFutureReqClient(ReqClient):

    def __init__(self):
        properties = configparser.ConfigParser()
        properties.read('C:/atm_collection_master/config.ini')
        database = properties["BINANCE"]
        api_key = database["API_KEY"]
        secret_key = database["SEC_KEY"]
        self.um_futures_client = UMFutures(key=api_key, secret=secret_key)

    def get_entry(self):
        coin_entry_list = list()
        for e in self.um_futures_client.exchange_info()['symbols']:
            c = CoinEntry()
            # c.exchange = 'BINANCE'
            c.symbol = e['symbol']
            c.status = e['status']
            c.base_asset = e['baseAsset']
            c.quote_asset = e['quoteAsset']
            c.base_asset_precision = e['baseAssetPrecision']
            c.quote_asset_precision = e['pricePrecision']
            c.onboard_date = e['onboardDate']
            # c = CoinEntry.create(
            #     exchange='BINANCE',
            #     symbol=e['symbol'],
            #     status=e['status'],
            #     base_asset=e['baseAsset'],
            #     quote_asset=e['quoteAsset'],
            #     base_asset_precision=e['baseAssetPrecision'],
            #     quote_asset_precision=e['pricePrecision'],
            #     onboard_date=e['onboardDate']
            # )
            coin_entry_list.append(c)
        return coin_entry_list

    def get_candle(self):
        pass

