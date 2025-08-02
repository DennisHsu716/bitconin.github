def save_order_book_snapshot(order_book, symbol):
    import json
    from datetime import datetime
    filename = f"orderbook_{symbol.replace('/','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(order_book, f)
    print(f"Order book snapshot saved as {filename}")
