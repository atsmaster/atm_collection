import peewee
from model.CoinEntryHist import CoinEntryHist


class CoinEntryHistRepo:

    def select_coin_entry_hist_by_exchage(self, exchange):
        return list(CoinEntryHist.select()
                 .where(CoinEntryHist.exchange == exchange)
                 .group_by(CoinEntryHist.exchange, CoinEntryHist.symbol))

    def batch_insert(self, lst_coin_entry_hist):
        CoinEntryHist.bulk_create(lst_coin_entry_hist)
