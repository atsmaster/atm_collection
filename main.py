import logging

from client.model.CoinCandleBinanceMin import CoinCandleBinanceMin
from client.model.CoinEntryHist import CoinEntryHist
from client.model.CoinEntry import CoinEntry
from collection import CoinCollector
from db.Database import Database
from sample.Backtest import Backtest
import sys


def create_table():
    database = Database().conn()
    database.create_tables([CoinEntry, CoinEntryHist, CoinCandleBinanceMin])


def main(argv):
    create_table()
    aa = CoinCollector.CoinCollector('BINANCE')
    aa.collect_coin(one_req_limit=1500, interval_cd='1m', by_date=None)
    # aa.check_missing_candle()
    # bb = Backtest()
    # bb.testtest()



if __name__ == '__main__':
    print("START")
    logger = logging.getLogger()
    logging.basicConfig(filename='C:/atm_collection_master/atm_collection/log.txt'
                        , format='%(levelname)s:[%(asctime)s] %(message)s'
                        , level=logging.INFO)
    main(sys.argv)

