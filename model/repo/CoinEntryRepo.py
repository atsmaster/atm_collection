import peewee
from model.CoinEntry import CoinEntry

class CoinEntryRepo:

    def select_by_exchage(self, exchange):
        return list(CoinEntry.select()
                    .where(CoinEntry.exchange == exchange))

    def batch_insert(self, lst_coin_entry):
        CoinEntry.bulk_create(lst_coin_entry)

