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
from com.ComDate import ComDate

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
        entry = list(self.coin_entry
                     .select(self.coin_entry.symbol, self.coin_entry.onboard_date)
                     .where(self.coin_entry.exchange == self.exchange))

        for e in entry:
            entry_info = (self.coin_candle
                              .select(self.coin_candle.symbol
                                      , peewee.fn.Max(self.coin_candle.open_time).alias('max_open_time')
                                      , peewee.fn.Min(self.coin_candle.open_time).alias('min_open_time')
                                      , peewee.fn.Count(self.coin_candle.open_time).alias('cnt_open_time')).limit(1)
                              .where(self.coin_candle.symbol == e.symbol)
                              .group_by(self.coin_candle.symbol, self.coin_candle.time_interval))

            # max_o = entry_info.max_open_time
            # min_o = entry_info['min_open_time']
            # cnt_o = entry_info.cnt_open_time
            #
            # print(max_o)
            # print(min_o)
            # print(cnt_o)


    def collect_coin(self, one_req_limit=None, interval_cd=None, by_date=None):
        """ collect_coin:

            Args:
                self :

            Returns:
                void :
                :param one_req_limit:
                :param interval_cd:
                :param by_date:
        """

        # 수집 종료 시간
        # by_date is not null   : 파라미터 일시   (한번돌고 끝)
        # by_date is null       : 현재일시 ~     (무한루프)
        is_loop = False
        if by_date is None:
            by_date = dt.datetime.now()
            is_loop = True

        # 수집시작
        while True:
            # 캔들 수집 전에 종목 수집 (상장 폐지, 신규 상장 등 확인을 위함)
            self.collect_entry()

            # 수집 가능 종목만 조회
            entry = list(self.coin_entry
                         .select(self.coin_entry.symbol, self.coin_entry.onboard_date)
                         .where(self.coin_entry.exchange == self.exchange))

            # 수집 시작 시간
            # - 거래소 기준 상장 일시  (첫 수집)
            # - DB 기준 가장 최근 일시 (이전 수집 기록 있음)
            max_open_time = list(self.coin_candle
                                 .select(self.coin_candle.symbol, self.coin_candle.time_interval,
                                         peewee.fn.Max(self.coin_candle.open_time))
                                 .group_by(self.coin_candle.symbol, self.coin_candle.time_interval))

            max_open_time = {x.symbol: x.open_time for x in max_open_time}

            for e in entry:
                if e.symbol in max_open_time.keys():
                    e.onboard_date = max_open_time[e.symbol] + ComDate.get_interval_val(interval_cd)

                self.collect_candle(e.symbol, e.onboard_date, by_date, interval_cd, one_req_limit)

            if is_loop is False:
                break

            by_date = dt.datetime.now()


    def collect_candle(self, symbol, start_date, end_date, interval_cd, one_req_limt):
        """ collect_candle:

            Args:
                self :

            Returns:
                void :
        """
        interval_val = ComDate.get_interval_val(interval_cd)

        temp_start_date = start_date
        temp_end_date = start_date + (interval_val * one_req_limt) - interval_val
        while True:
            if temp_end_date > end_date:
                candle = self.req_client.get_candle(symbol, interval_cd, temp_start_date, end_date, one_req_limt)
                self.coin_candle.bulk_create(candle)
                break
            else:
                candle = self.req_client.get_candle(symbol, interval_cd, temp_start_date, temp_end_date, one_req_limt)
                self.coin_candle.bulk_create(candle)

            temp_start_date = temp_start_date + (interval_val * one_req_limt)
            temp_end_date = temp_end_date + (interval_val * one_req_limt)
            time.sleep(0.5)

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
                .where(self.coin_entry_hist.exchange == self.exchange)
                .group_by(self.coin_entry_hist.exchange, self.coin_entry_hist.symbol))

        req_entry_dict = dict()
        db_entry_dict = dict()
        db_entry_hist_set = set()

        # 요청(거래소 API)된 종목 정보
        for req_entry in req_entry_s:
            req_entry_dict[req_entry.symbol] = req_entry

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


# aa = CoinCollector('BINANCE')
# # aa.collect_entry()
# aa.collect_candle_n()
# # aa.collect_candle_l()
