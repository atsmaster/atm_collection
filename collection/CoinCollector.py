import datetime
import logging

from peewee import fn

from client.ReqClientFactory import ReqClientFactory
from client.model.CoinCandleFactory import CoinCandleFactory
from client.model.CoinEntry import CoinEntry
from client.model.CoinEntryStatus import CoinEntryStatus

logger = logging.getLogger()
logging.basicConfig(format='%(levelname)s:[%(asctime)s] %(message)s', level=logging.DEBUG)


class CoinCollector:
    """ CoinCollector:
            Coin의 정보, 상태, 가격 등을 수집하는 클래스입니다.

        __init__:
            거래소(exchange)를 파라미터로 받아 해당 거래소의 정보를 처리합니다.
    """

    def __init__(self, exchange):
        self.exchange = exchange
        self.req_client = ReqClientFactory.create_req(exchange)
        self.coin_candle = CoinCandleFactory.create_entry(exchange)
        self.coin_entry = CoinEntry
        self.coin_entry_status = CoinEntryStatus

    def collect_candle_n(self):
        sub = self.coin_entry_status \
            .select(self.coin_entry_status.symbol) \
            .where(self.coin_entry_status.exchange == self.exchange, self.coin_entry_status.list_cd == 'N')

        entry_list_onboard = list(self.coin_entry
                                  .select(self.coin_entry.symbol, self.coin_entry.onboard_date)
                                  .where(self.coin_entry.symbol.in_(sub)))

        entry_list_maxopentime = list(self.coin_candle
                                      .select(self.coin_candle.symbol, self.coin_candle.time_interval, fn.Max(self.coin_candle.open_time))
                                      .where(self.coin_candle.symbol.in_(sub))
                                      .group_by(self.coin_candle.symbol, self.coin_candle.time_interval))

        now_date = datetime.datetime.now()
        import time
        start = time.time()  # 시작 시간 저장
        for entry in entry_list_onboard:
            base_date = entry.onboard_date

            start_date = base_date
            end_date = base_date + datetime.timedelta(minutes=1500)
            while True:
                if end_date >= now_date:
                    end_date = now_date
                    candle = self.req_client.get_candle(entry.symbol, '1m', start_date, end_date, 1500)
                    self.coin_candle.bulk_create(candle)
                    break

                candle = self.req_client.get_candle(entry.symbol, '1m', start_date, end_date, 1500)
                # self.coin_candle.bulk_create(candle)
                logger.info("%s / %s ~ %s", entry.symbol, start_date, end_date)
                # print("[%s] %s ~ %s", entry.symbol, start_date, end_date)

                start_date = end_date + datetime.timedelta(minutes=1)
                end_date = start_date + datetime.timedelta(minutes=1500)

    def collect_candle_l(self):
        sub = self.coin_entry_status \
            .select(self.coin_entry_status.symbol) \
            .where(self.coin_entry_status.exchange == self.exchange, self.coin_entry_status.list_cd == 'L')

        entry_list = self.coin_candle \
            .select(self.coin_candle.symbol, fn.Max(self.coin_candle.open_time)) \
            .where(self.coin_candle.symbol.in_(sub)) \
            .group_by(self.coin_candle.symbol)

        # 현재 상장중(L)인 종목에 대해서만 가격요청, 가장 최근에 저장된 Time 부터
        for entry in entry_list:
            self.req_client.get_candle(['1000LUNCBUSD'], '1m', entry.onboard_date, entry.onboard_date)

        # for entry in entry_list:
        #     print(entry)
        #     self.req_client.get_candle(entry)

    def collect_entry(self):
        """ update_entry:
                거래소API를 요청하여 신규 상장, 상장 폐지, 기존 상장 종목 들을 insert, update 한다.

            Args:
                self :

            Returns:
                void :
        """
        req_entry_s = self.req_client.get_entry()
        db_entry_s = self.coin_entry.select()
        req_entry_dict = dict()
        db_entry_dict = dict()

        # 요청(거래소 API)된 종목 정보
        for req_entry in req_entry_s:
            req_entry_dict[req_entry.symbol] = req_entry

        # DB에 조회된 종목 정보
        for db_entry in db_entry_s:
            db_entry_dict[db_entry.symbol] = db_entry

        existing_entry_symbol = req_entry_dict.keys() & db_entry_dict.keys()  # 기존 종목
        new_entry_symbol = req_entry_dict.keys() - db_entry_dict.keys()  # 상장 신규 종목
        del_entry_symbol = db_entry_dict.keys() - req_entry_dict.keys()  # 상장 폐지 종목

        update_coin_entry = list()
        insert_coin_entry = list()
        update_coin_entry_status = list()
        insert_coin_entry_status = list()
        # 기존 종목, 상장 신규 종목, 상장 폐지 종목 처리
        for symbol, entry in req_entry_dict.items():
            if symbol in existing_entry_symbol and entry.__ne__(db_entry_dict[symbol]):
                update_coin_entry.append(entry)

            if symbol in new_entry_symbol:
                insert_coin_entry.append(entry)

        for symbol in new_entry_symbol:
            status = CoinEntryStatus()
            status.exchange = self.exchange
            status.symbol = symbol
            status.list_cd = 'N'
            status.price_use_yn = False
            insert_coin_entry_status.append(status)

        for symbol in del_entry_symbol:
            status = CoinEntryStatus()
            status.exchange = self.exchange
            status.symbol = symbol
            status.list_cd = 'D'
            status.price_use_yn = False
            update_coin_entry_status.append(status)

        # 정보 저장
        if len(insert_coin_entry) > 0:
            self.coin_entry.bulk_create(insert_coin_entry)
        if len(insert_coin_entry_status) > 0:
            self.coin_entry_status.bulk_create(insert_coin_entry_status)

        if len(update_coin_entry) > 0:
            for e in update_coin_entry:
                e.save()
        if len(update_coin_entry_status) > 0:
            for e in update_coin_entry_status:
                e.save()


aa = CoinCollector('BINANCE')
aa.collect_entry()
# aa.collect_candle_n()
# aa.collect_candle_l()
