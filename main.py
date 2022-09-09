import logging

from client.model.CoinCandleBinance import CoinCandleBinance
from client.model.CoinEntryStatus import CoinEntryStatus
from client.model.CoinEntry import CoinEntry
from db.Database import Database
import sys


def create_table():
    database = Database().conn()
    database.create_tables([CoinEntry, CoinEntryStatus, CoinCandleBinance])
    aa=0


def main(argv):
    create_table()
    # CoinCollector('BINANCE')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv)

