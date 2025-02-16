import ccxt

def get_price(exchange, symbol):
    """ Получаем цену криптовалюты на бирже """
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']  # Последняя цена сделки
    except Exception as e:
        print(f"Ошибка получения цены с {exchange.id}: {e}")
        return None

def get_all_pairs(exchange):
    """ Получаем список всех торговых пар на бирже """
    try:
        markets = exchange.load_markets()
        return list(markets.keys())
    except Exception as e:
        print(f"Ошибка загрузки рынков с {exchange.id}: {e}")
        return []

# Подключаем биржу Kraken с демо-счетом
exchange = ccxt.kraken({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
    'password': 'YOUR_PASSWORD',
    'options': {
        'sandbox': True  # Включаем режим демо-торговли
    }
})

# Получаем все торговые пары
pairs = get_all_pairs(exchange)

# Проверяем арбитражные возможности
for pair1 in pairs:
    for pair2 in pairs:
        if pair1 != pair2:
            price1 = get_price(exchange, pair1)
            price2 = get_price(exchange, pair2)
            if price1 and price2:
                spread = abs(price1 - price2) / min(price1, price2) * 100
                if spread > 0.5:  # Условие минимальной разницы
                    print(f"Арбитражная возможность: {pair1} -> {pair2} (разница {spread:.2f}%)")

print("Анализ завершен.")
