import logging

from model.CoinCandleBinanceMin import CoinCandleBinanceMin
from model.CoinEntryHist import CoinEntryHist
from model.CoinEntry import CoinEntry
from collection import CoinCollector
from config.DatabaseConfig import Database
import sys


def create_table():
    database = Database().conn()
    database.create_tables([CoinEntry, CoinEntryHist, CoinCandleBinanceMin])


def main(argv):
    create_table()
    # aa = CoinCollector.CoinCollector('BINANCE')
    # aa.collect_coin(one_req_limit=1500, interval_cd='1m', by_date=None)
    # aa.check_missing_candle()
    # bb = Backtest()
    # bb.testtest()

    collector = CoinCollector.CoinCollector('BINANCE')
    collector.collect_entry()




if __name__ == '__main__':
    print("START")
    logger = logging.getLogger()
    logging.basicConfig(filename='D:/atm_master/atm_collection/log.txt'
                        , format='%(levelname)s:[%(asctime)s] %(message)s'
                        , level=logging.INFO)
    main(sys.argv)

