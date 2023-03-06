import peewee
from model.CoinCandleBinanceMin import CoinCandleBinanceMin


class CoinCandleBinanceMinRepo:

    def select_group_by_symbol(self, symbol):
        return list(CoinCandleBinanceMin
                .select(CoinCandleBinanceMin.symbol
                        , peewee.fn.Max(CoinCandleBinanceMin.open_time).alias('max_open_time')
                        , peewee.fn.Min(CoinCandleBinanceMin.open_time).alias('min_open_time')
                        , peewee.fn.Count(CoinCandleBinanceMin.open_time).alias('cnt_open_time')).limit(1)
                .where(CoinCandleBinanceMin.symbol == symbol)
                .group_by(CoinCandleBinanceMin.symbol))

    def select_group_max_open_time(self):
        return list(CoinCandleBinanceMin
             .select(CoinCandleBinanceMin.symbol,
                     peewee.fn.Max(CoinCandleBinanceMin.open_time))
             .group_by(CoinCandleBinanceMin.symbol))

