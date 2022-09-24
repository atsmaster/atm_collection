import datetime as dt
import logging
import os
import sys
import time
import peewee

from client.ReqClientFactory import ReqClientFactory
from client.binance.future.BnFutureWssClient import BnFutureWssClient
from client.model.CoinCandleFactory import CoinCandleFactory
from client.model.CoinEntry import CoinEntry
from client.model.CoinEntryHist import CoinEntryHist

logger = logging.getLogger()


class CoinCollector:
    """ CoinCollector:
            Coin의 정보, 상태, 가격 등을 수집하는 클래스입니다.

        __init__:
            거래소(exchange)를 파라미터로 받아 해당 거래소의 정보를 처리합니다.
    """

    def __init__(self, exchange):
        self.exchange = exchange
        self.req_client = ReqClientFactory.create_req(exchange)
        self.wss_client = BnFutureWssClient()
        self.coin_candle = CoinCandleFactory.create_entry(exchange)
        self.coin_entry = CoinEntry
        self.coin_entry_hist = CoinEntryHist

    def check_missing_candle(self):
        """ check_missing_candle:
                신규 상장 종목 대상으로 결측치(missing value)가 있는지 확인

            Args:
                self :

            Returns:
                void :
        """

        sub = (self.coin_entry_status
                    .select(self.coin_entry_status.symbol)
                    .where(self.coin_entry_status.exchange == self.exchange, self.coin_entry_status.list_cd == 'N'))

        entry_list_maxopentime = list(self.coin_candle
                                      .select(self.coin_candle.symbol
                                              , peewee.fn.Max(self.coin_candle.open_time).alias('max_open_time')
                                              , peewee.fn.Min(self.coin_candle.open_time).alias('min_open_time')
                                              , peewee.fn.Count(self.coin_candle.open_time)).alias('cnt_open_time')
                                      .where(self.coin_candle.symbol.in_(sub))
                                      .group_by(self.coin_candle.symbol, self.coin_candle.time_interval))

    def collect_candle_n(self):
        """ collect_candle_n:
                거래소에 요청하여 신규 상장(N)한 종목의 캔들을 저장한다.
                1. 상장일부터 수집
                2. 신규지만 DB에 저장되어 있다면(수집중 종료하게되면 이런 경우가 있음), 가장최근 open_time 부터 수집

            Args:
                self :

            Returns:
                void :
        """
        sub = (self.coin_entry_status
                    .select(self.coin_entry_status.symbol)
                    .where(self.coin_entry_status.exchange == self.exchange, self.coin_entry_status.list_cd == 'N'))

        entry_list_onboard = list(self.coin_entry
                                  .select(self.coin_entry.symbol, self.coin_entry.onboard_date)
                                  .where(self.coin_entry.symbol.in_(sub)))

        entry_list_maxopentime = list(self.coin_candle
                                      .select(self.coin_candle.symbol, self.coin_candle.time_interval, peewee.fn.Max(self.coin_candle.open_time))
                                      .where(self.coin_candle.symbol.in_(sub))
                                      .group_by(self.coin_candle.symbol, self.coin_candle.time_interval))

        entry_list_maxopentime = {x.symbol: x.open_time for x in entry_list_maxopentime}

        now_date = dt.now()

        start = time.time()  # 시작 시간 저장
        for entry in entry_list_onboard:
            base_date = entry.onboard_date
            if entry.symbol in entry_list_maxopentime:  # 기존에 캔들 데이터가 존재한다면 가장 최근 open time 부터 수집
                base_date = entry_list_maxopentime[entry.symbol] + dt.timedelta(minutes=1)

            start_date = base_date
            end_date = base_date + dt.timedelta(minutes=1500)
            while True:
                if end_date >= now_date:
                    end_date = now_date
                    candle = self.req_client.get_candle(entry.symbol, '1m', start_date, end_date, 1500)
                    self.coin_candle.bulk_create(candle)
                    logger.info("%s / %s ~ %s", entry.symbol, start_date, end_date)
                    break

                candle = self.req_client.get_candle(entry.symbol, '1m', start_date, end_date, 1500)
                self.coin_candle.bulk_create(candle)
                logger.info("%s / %s ~ %s", entry.symbol, start_date, end_date)
                # print("[%s] %s ~ %s", entry.symbol, start_date, end_date)

                start_date = end_date + dt.timedelta(minutes=1)
                end_date = start_date + dt.timedelta(minutes=1500)
                time.sleep(0.5)

    def collect_candle_l(self):
        """ collect_candle_l:
                거래소에 요청하여 기존 상장중(L)인 종목의 캔들을 저장한다.
                1. DB에 저장되어 캔들 중 종목마다 가장 최근 open_time을 기준으로 캔들 저장

            Args:
                self :

            Returns:
                void :
        """

        # 수집 가능한 종목명
        entry = self.coin_entry.select(self.coin_entry.symbol).where(self.coin_entry.exchange == self.exchange)
        symbol_set = {e.symbol for e in entry}

        now = dt.datetime.now()
        temp_date = dt.datetime(now.year, now.month, now.day, now.hour, now.minute)

        while True:
            entry_list = list(self.coin_candle
                              .select(self.coin_candle.symbol
                                      , peewee.fn.Max(self.coin_candle.open_time).alias('max_open_time'))
                              .group_by(self.coin_candle.symbol, self.coin_candle.time_interval))

            for e in entry_list:  # temp_date 기준으로 캔들 삽입
                if e in symbol_set:  # 수집 가능한 종목 체크
                    continue

                start_date = e.max_open_time
                end_date = start_date + dt.timedelta(minutes=1500)
                req_date_list = []
                while True:
                    if end_date > temp_date:
                        end_date = temp_date
                        req_date_list.append([start_date, end_date])
                        break

                    req_date_list.append([start_date, end_date])
                    start_date = start_date + dt.timedelta(minutes=1501)
                    end_date = end_date + dt.timedelta(minutes=1501)

                for d in req_date_list:
                    candle = self.req_client.get_candle(e.symbol, '1m', d[0], d[1], 1500)
                    self.coin_candle.bulk_create(candle)
                    time.sleep(0.5)



            now = dt.datetime.now()
            temp_date = dt.datetime(now.year, now.month, now.day, now.hour, now.minute)




        # # 현재 상장중(L)인 종목에 대해서만 가격요청, 가장 최근에 저장된 Time 부터
        # for entry in entry_list:
        #     self.req_client.get_candle(['1000LUNCBUSD'], '1m', entry.onboard_date, entry.onboard_date)

        # for entry in entry_list:
        #     print(entry)
        #     self.req_client.get_candle(entry)

    def collect_entry(self):
        """ update_entry:
                거래소에 요청하여 신규 상장, 상장 폐지, 기존 상장 종목 들을 insert, update 한다.

            Args:
                self :

            Returns:
                void :
        """
        req_entry_s = self.req_client.get_entry()
        db_entry_s = self.coin_entry.select()
        db_entry_hist_s = (self.coin_entry_hist.select()
                .group_by(self.coin_entry_hist.exchange, self.coin_entry_hist.symbol))

        req_entry_dict = dict()
        db_entry_dict = dict()
        db_entry_hist_set = set()

        # 요청(거래소 API)된 종목 정보
        for req_entry in req_entry_s:
            req_entry_dict[req_entry.symbol] = req_entry

        req_entry_dict.pop('1000LUNCBUSD')

        # DB에 조회된 종목 정보
        for db_entry in db_entry_s:
            db_entry_dict[db_entry.symbol] = db_entry

        # DB에 조회된 종목 hist 종목명
        for db_entry_hist in db_entry_hist_s:
            db_entry_hist_set.add(db_entry_hist.symbol)

        existing_entry_symbol = req_entry_dict.keys() & db_entry_dict.keys()  # 기존 종목
        new_entry_symbol = req_entry_dict.keys() - db_entry_dict.keys()  # 상장 신규 종목 (+ 재상장)
        del_entry_symbol = db_entry_dict.keys() - req_entry_dict.keys()  # 상장 폐지 종목

        insert_coin_entry = list()
        update_coin_entry = list()
        delete_coin_entry = list()
        insert_coin_entry_hist = list()

        for symbol in new_entry_symbol:
            if symbol in db_entry_hist_set:
                hist = self.create_coin_entry_hist(req_entry_dict[symbol], 'R', 'Y')
                insert_coin_entry_hist.append(hist)
            else:
                hist = self.create_coin_entry_hist(req_entry_dict[symbol], 'N', 'Y')
                insert_coin_entry_hist.append(hist)

            insert_coin_entry.append(req_entry_dict[symbol])

        for symbol in existing_entry_symbol:
            if req_entry_dict[symbol].__ne__(db_entry_dict[symbol]):
                hist = self.create_coin_entry_hist(req_entry_dict[symbol], 'L', 'Y')
                insert_coin_entry_hist.append(hist)
                update_coin_entry.append(req_entry_dict[symbol])

        for symbol in del_entry_symbol:
            hist = self.create_coin_entry_hist(db_entry_dict[symbol], 'D', 'Y')
            insert_coin_entry_hist.append(hist)
            delete_coin_entry.append(db_entry_dict[symbol])

        if len(insert_coin_entry) > 0:
            self.coin_entry.bulk_create(insert_coin_entry)

        if len(insert_coin_entry_hist) > 0:
            self.coin_entry_hist.bulk_create(insert_coin_entry_hist)

        for e in update_coin_entry:
            e.save()

        for e in delete_coin_entry:
            e.delete_instance()

    def create_coin_entry_hist(self, entry, list_cd, price_yn):
        hist = CoinEntryHist()
        hist.exchange = self.exchange
        hist.symbol = entry.symbol
        hist.status = entry.status
        hist.base_asset = entry.base_asset
        hist.quote_asset = entry.quote_asset
        hist.base_asset_precision = entry.base_asset_precision
        hist.quote_asset_precision = entry.quote_asset_precision
        hist.onboard_date = entry.onboard_date
        hist.list_cd = list_cd
        hist.price_use_yn = price_yn
        return hist



        # # 기존 종목, 상장 신규 종목, 상장 폐지 종목 처리
        # for symbol, entry in req_entry_dict.items():
        #     if symbol in existing_entry_symbol and entry.__ne__(db_entry_dict[symbol]):
        #         update_coin_entry.append(entry)
        #
        #     if symbol in new_entry_symbol:
        #         insert_coin_entry.append(entry)
        #
        # for symbol in new_entry_symbol:
        #     status = CoinEntryHist()
        #     status.exchange = self.exchange
        #     status.symbol = symbol
        #     status.list_cd = 'N'
        #     status.price_use_yn = False
        #     insert_coin_entry_status.append(status)
        #
        # for symbol in del_entry_symbol:
        #     status = CoinEntryHist()
        #     status.exchange = self.exchange
        #     status.symbol = symbol
        #     status.list_cd = 'D'
        #     status.price_use_yn = False
        #     update_coin_entry_status.append(status)
        #
        # # 정보 저장
        # if len(insert_coin_entry) > 0:
        #     self.coin_entry.bulk_create(insert_coin_entry)
        # if len(insert_coin_entry_status) > 0:
        #     self.coin_entry_status.bulk_create(insert_coin_entry_status)
        #
        # if len(update_coin_entry) > 0:
        #     for e in update_coin_entry:
        #         e.save()
        # if len(update_coin_entry_status) > 0:
        #     for e in update_coin_entry_status:
        #         e.save()


# aa = CoinCollector('BINANCE')
# # aa.collect_entry()
# aa.collect_candle_n()
# # aa.collect_candle_l()
