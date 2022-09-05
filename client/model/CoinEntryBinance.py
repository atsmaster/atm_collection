from client.model.CoinEntry import CoinEntry


class CoinEntryBinance(CoinEntry):
    class Meta:
        db_table = 'coin_entry_binance'
