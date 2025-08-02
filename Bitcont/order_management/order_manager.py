class OrderManager:
    def __init__(self, connector):
        self.connector = connector


    def place_order(self, symbol, side, amount, order_type="limit", price=None):
        pass

    def cancel_order(self, order_id):
        pass

    def get_order_status(self, order_id):
        pass
