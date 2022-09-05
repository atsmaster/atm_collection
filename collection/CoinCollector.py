from client.ReqClientFactory import ReqClientFactory
from client.model.CoinEntryFactory import CoinEntryFactory
from client.model.CoinEntry import CoinEntry
import time


class CoinCollector:

    def __init__(self, exchange):
        self.req_client = ReqClientFactory.create_req(exchange)
        self.coin_entry = CoinEntryFactory.create_entry(exchange)

    def update_entry(self):
        req_entry_s = self.req_client.get_entry()
        db_entry_s = self.coin_entry.select(self.coin_entry.symbol)
        req_entry_set = set()
        db_entry_set = set()

        # 요청(거래소 API)된 종목 정보
        for req_entry in req_entry_s:
            req_entry_set.add(req_entry.symbol)

        # DB에 조회된 종목 정보
        for db_entry in db_entry_s:
            db_entry_set.add(db_entry.symbol)

        existing_entry = req_entry_set & db_entry_set   # 기존 종목
        listing_entry = req_entry_set - db_entry_set    # 상장 신규 종목
        delisting_entry = db_entry_set - req_entry_set  # 상장 폐지 종목


aa = CoinCollector('BINANCE')
aa.update_entry ()
