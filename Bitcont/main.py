import sys
import time
sys.path.append('.')


# Import connectors for each supported exchange
from connectors.kucoin_connector import KucoinConnector    # Kucoin Exchange
from connectors.bitmart_connector import BitmartConnector  # Bitmart Exchange
from connectors.okx_connector import OKXConnector          # OKX Exchange
from connectors.deriv_connector import DerivConnector      # Deriv Exchange
from connectors.binance_connector import BinanceConnector  # Binance Exchange

from order_management.order_manager import OrderManager     # Handles order placement and status queries
from monitoring.position_monitor import get_position_details # Position and PnL monitoring
from utils.symbol_mapper import map_symbol                  # Symbol mapping utility
from utils.data_persistence import save_order_book_snapshot # Utility for saving historical order book data


def map_symbol(exchange, symbol):
    """
    Return the exchange-specific symbol for a given exchange and standard symbol.
    Args:
        exchange (str): The name of the exchange
        symbol (str): The standard symbol
    Returns:
        str: The symbol format used by the exchange.
    """
    mapping = {'binance': {'BTC/USDT': 'BTC/USDT'}, 'bitmart': {'BTC/USDT': 'BTC/USDT'},'kucoin': {'BTC/USDT': 'BTC-USDT'}, 'okx': {'BTC/USDT': 'BTC-USDT'},'deriv': {'BTC/USDT': 'BTC/USD'}}
    return mapping.get(exchange, {}).get(symbol, symbol)


# All supported exchanges with their connector classes
connector_classes = [('binance', BinanceConnector), ('bitmart', BitmartConnector),('kucoin', KucoinConnector),('okx', OKXConnector),('deriv', DerivConnector)]






def demo_cross_exchange_workflow():
    """
    Main workflow: Execute all Tasks for each exchange and prints out the results for every step.
    """
    symbol_std = 'BTC/USDT'  # Standard trading pair symbol used for all exchanges

    # Loop over all supported exchange connectors
    for name, Cls in connector_classes:
        print("=" * 60)
        print(f"======  {name.upper()}  ======")  # Print the current exchange name
        connector = Cls()
        symbol = map_symbol(name, symbol_std) # Map the standard symbol to the exchange-specific format

        # Task 1: Fetch market data
        order_book = None
        bid, ask = None, None
        try:
            # Fetch order book and best bid/ask
            order_book = connector.fetch_order_book(symbol)
            bid, ask = connector.fetch_best_bid_ask(symbol)
            print(f"[Task1] {name}: Best Bid: {bid}, Best Ask: {ask}")
        except Exception as e:
            print(f"[Task1] {name} error: {e}")

        # Task 2: Place order and check order status
        order_id = None
        order_status = None
        try:
            if bid is not None:
                order_manager = OrderManager(connector)
                # Place a limit buy order at the current best bid
                order_id = order_manager.place_order(symbol, side="buy", amount=0.001, order_type="limit", price=bid)
                print(f"[Task2] {name}: Order ID: {order_id}")
                time.sleep(1)
                # Query order status
                order_status = order_manager.get_order_status(order_id)
                print(f"[Task2] {name}: Order Status: {order_status}")
            else:
                print(f"[Task2] {name}: Cannot place order, bid is None.")
        except Exception as e:
            print(f"[Task2] {name} error: {e}")

        # Task 3: Monitor position and PnL
        try:
            if order_id is not None:
                # Query the position for the given order
                position = get_position_details(connector, symbol, order_id)
                print(f"[Task3] {name}: Position Info: {position}")
            else:
                print(f"[Task3] {name}: No valid order_id for PnL monitoring.")
        except Exception as e:
            print(f"[Task3] {name} error: {e}")

        # Task 4: Symbol mapping
        print(f"[Task4] {name}: Symbol mapping: exchange symbol = {symbol}, standard symbol = {symbol_std}")

        # Task 5: Save historical order book snapshot
        if order_book is not None:
            try:
                # Save the order book snapshot as a JSON file
                save_order_book_snapshot(order_book, f"{name}-{symbol}")
                print(f"[Task5] {name}: Order book snapshot saved.")
            except Exception as e:
                print(f"[Task5] {name} error: {e}")
        else:
            print(f"[Task5] {name}: No order book to save.")

if __name__ == "__main__":
    demo_cross_exchange_workflow()
