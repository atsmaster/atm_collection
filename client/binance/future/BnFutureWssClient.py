import logging
import time

from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

from client.model.CoinCandleBinance import CoinCandleBinance

logger = logging.getLogger()


class BnFutureWssClient:

    EXCHANGE_NAME = 'BINANCE'

    def __init__(self):
        self.client = UMFuturesWebsocketClient()
        self.client.start()
        self.candles = dict()

