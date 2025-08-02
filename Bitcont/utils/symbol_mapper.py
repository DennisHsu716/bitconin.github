def map_symbol(exchange, symbol):
    mapping = {
        'binance': {'BTC/USDT': 'BTC/USDT'},
        'kucoin': {'BTC/USDT': 'BTC-USDT'},
    }
    return mapping.get(exchange, {}).get(symbol, symbol)
