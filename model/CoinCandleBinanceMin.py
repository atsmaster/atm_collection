from model.CoinCandle import CoinCandle


class CoinCandleBinanceMin(CoinCandle):

    class Meta:
        db_table = 'TB_COIN_CANDLE_BINANCE_MIN'


