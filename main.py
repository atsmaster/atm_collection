import logging

from client.model.CoinCandleBinance import CoinCandleBinance
from client.model.CoinEntryStatus import CoinEntryStatus
from client.model.CoinEntry import CoinEntry
from collection import CoinCollector
from db.Database import Database
import sys


def create_table():
    database = Database().conn()
    database.create_tables([CoinEntry, CoinEntryStatus, CoinCandleBinance])
    aa = 0


def main(argv):
    create_table()
    aa = CoinCollector.CoinCollector('BINANCE')
    aa.collect_candle_n()


if __name__ == '__main__':
    print("START")
    logger = logging.getLogger()
    logging.basicConfig(filename='C:/atm_collection_master/atm_collection/log.txt'
                        , format='%(levelname)s:[%(asctime)s] %(message)s'
                        , level=logging.INFO)
    main(sys.argv)

