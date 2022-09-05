from client.model.CoinEntry import CoinEntry
from client.model.CoinEntryBinance import CoinEntryBinance
from db.Database import Database
import sys


def create_table():
    database = Database().conn()
    database.create_tables([CoinEntryBinance])
    aa=0


def main(argv):
    create_table()
    # CoinCollector('BINANCE')


if __name__ == '__main__':
    main(sys.argv)

