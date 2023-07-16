import configparser
from datetime import datetime

from binance.um_futures import UMFutures
from client.ReqClient import ReqClient
from model.CoinCandleBinanceMin import CoinCandleBinanceMin
from model.CoinEntry import CoinEntry


class BnFutureReqClient(ReqClient):

    EXCHANGE_NAME = 'BINANCE'
    LIMIT = 2400  # 분당 요청할 수 있는 개수

    def __init__(self):
        properties = configparser.ConfigParser()
        properties.read('D:/atm_master/config.ini')
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
            c.symbol_status_cd = e['status']
            c.base_asset = e['baseAsset']
            c.quote_asset = e['quoteAsset']
            c.base_asset_precision = e['baseAssetPrecision']
            c.quote_asset_precision = e['pricePrecision']
            c.onboard_dttm = datetime.fromtimestamp(e['onboardDate']/1000)
            coin_entry_list.append(c)
        return coin_entry_list

    def get_candle(self, symbol, interval, start_time, end_time, limit):
        # print(start_time)
        # print(start_time.replace(tzinfo=timezone.utc))
        # print(start_time.timestamp())
        # print(start_time.replace(tzinfo=timezone.utc).timestamp())

        start_time = int(start_time.timestamp() * 1000)
        end_time = int(end_time.timestamp() * 1000)

        candle_list = list()
        for e in self.um_futures_client.klines(
                symbol=symbol, interval=interval, startTime=start_time, endTime=end_time, limit=limit):
            c = CoinCandleBinanceMin()
            c.symbol = symbol
            c.open_dttm = datetime.fromtimestamp(int(e[0] / 1000))
            c.open = e[1]
            c.close = e[4]
            c.high = e[2]
            c.low = e[3]
            candle_list.append(c)

        return candle_list
