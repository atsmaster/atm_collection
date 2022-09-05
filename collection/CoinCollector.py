from client.ReqClientFactory import ReqClientFactory
from client.model.CoinEntryFactory import CoinEntryFactory
from client.model.CoinEntry import CoinEntry
import time

from client.model.CoinEntryStatus import CoinEntryStatus
import time


class CoinCollector:

    def __init__(self, exchange):
        self.exchange = exchange
        self.req_client = ReqClientFactory.create_req(exchange)
        self.coin_entry = CoinEntryFactory.create_entry(exchange)
        self.coin_entry_status = CoinEntryStatus

    def update_entry(self):
        start = time.time()  # 시작 시간 저장

        req_entry_s = self.req_client.get_entry()
        db_entry_s = self.coin_entry.select(self.coin_entry.symbol)
        req_entry_dict = dict()
        db_entry_dict = dict()

        # self.coin_entry.bulk_create(req_entry_s)

        # 요청(거래소 API)된 종목 정보
        for req_entry in req_entry_s:
            req_entry_dict[req_entry.symbol] = req_entry

        # DB에 조회된 종목 정보
        for db_entry in db_entry_s:
            db_entry_dict[db_entry.symbol] = db_entry

        existing_entry_symbol = req_entry_dict.keys() & db_entry_dict.keys()   # 기존 종목
        listing_entry_symbol = req_entry_dict.keys() - db_entry_dict.keys()    # 상장 신규 종목
        delisting_entry_symbol = db_entry_dict.keys() - req_entry_dict.keys()  # 상장 폐지 종목

        update_coin_entry = list()
        insert_coin_entry = list()
        update_coin_entry_status = list()
        insert_coin_entry_status = list()
        for symbol, entry in req_entry_dict.items():
            if symbol in existing_entry_symbol and not entry == db_entry_dict[symbol]:
                update_coin_entry.append(entry)

            if symbol in listing_entry_symbol:
                insert_coin_entry.append(entry)

        for symbol in listing_entry_symbol:
            status = CoinEntryStatus()
            status.exchange = self.exchange
            status.symbol = symbol
            status.list_cd = 'N'
            status.price_use_yn = '0'
            insert_coin_entry_status.append(status)

        for symbol in delisting_entry_symbol:
            status = CoinEntryStatus()
            status.exchange = self.exchange
            status.symbol = symbol
            status.list_cd = 'D'
            status.price_use_yn = '0'
            update_coin_entry_status.append(status)

        if len(insert_coin_entry) > 0:
            self.coin_entry.bulk_create(insert_coin_entry)
        if len(update_coin_entry) > 0:
            self.coin_entry.bulk_update(update_coin_entry)
        if len(insert_coin_entry_status) > 0:
            self.coin_entry_status.bulk_create(insert_coin_entry_status)
        if len(update_coin_entry_status) > 0:
            self.coin_entry_status.bulk_update(update_coin_entry_status)

        print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간


aa = CoinCollector('BINANCE')
aa.update_entry()
