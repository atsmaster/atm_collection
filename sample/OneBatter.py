import time
import logging
from binance.lib.utils import config_logging
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
import configparser


config_logging(logging, logging.DEBUG)


def message_handler(message):
    print(message)


properties = configparser.ConfigParser()
properties.read('C:/atm_collection_master/config.ini')
database = properties["BINANCE"]
api_key = database["API_KEY"]

client = UMFutures(api_key)
response = client.new_listen_key()

logging.info("Listen key : {}".format(response["listenKey"]))

ws_client = UMFuturesWebsocketClient()
ws_client.start()

ws_client.user_data(
    listen_key=response["listenKey"],
    id=1,
    callback=message_handler,
)

# time.sleep(30)

logging.debug("closing ws connection")
ws_client.stop()