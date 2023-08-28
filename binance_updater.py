import time
from binance.client import Client
from binance.exceptions import BinanceAPIException

def update_binance_data(client, my_balances, open_orders):
    while True:
        try:
            if client is not None:
                account = client.futures_account()
                my_balances.clear()  # Clear existing balances
                my_balances.extend(account['assets'])
                open_orders.clear()  # Clear existing orders
                open_orders.extend(client.futures_get_open_orders(symbol=''))
        except BinanceAPIException as e:
            print(f"API error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(1)  # Wait for 10 seconds before updating again