import configparser
from datetime import datetime, timezone

from binance.um_futures import UMFutures
from client.ReqClient import ReqClient
from client.model.CoinEntry import CoinEntry


class BnFutureReqClient(ReqClient):

    EXCHANGE_NAME = 'BINANCE'
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
            c.exchange = self.EXCHANGE_NAME
            c.symbol = e['symbol']
            c.status = e['status']
            c.base_asset = e['baseAsset']
            c.quote_asset = e['quoteAsset']
            c.base_asset_precision = e['baseAssetPrecision']
            c.quote_asset_precision = e['pricePrecision']
            c.onboard_date = datetime.fromtimestamp(int(e['onboardDate']/1000))
            coin_entry_list.append(c)
        return coin_entry_list

    def get_candle(self, symbol_list, interval, start_time, end_time):
        print(start_time)
        print(start_time.replace(tzinfo=timezone.utc))
        print(start_time.timestamp())
        print(start_time.replace(tzinfo=timezone.utc).timestamp())


        # start_time = int(start_time.replace(tzinfo=timezone.utc).timestamp())
        # end_time = int(end_time.replace(tzinfo=timezone.utc).timestamp())

        for symbol in symbol_list:
            aa = self.um_futures_client.klines(symbol=symbol, interval=interval, startTime=start_time, endTime=end_time)
            print('aab')
