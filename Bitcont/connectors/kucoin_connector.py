import ccxt


class KucoinConnector:
    def __init__(self):
        self.exchange = ccxt.kucoin()

    def fetch_order_book(self, symbol):
        return self.exchange.fetch_order_book(symbol)

    def fetch_best_bid_ask(self, symbol):
        ob = self.fetch_order_book(symbol)
        bid = ob['bids'][0][0] if ob['bids'] else None
        ask = ob['asks'][0][0] if ob['asks'] else None
        return bid, ask
