import config, csv
from binance.client import Client
from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from binance.enums import *
from binance.exceptions import BinanceAPIException

from flask import Flask, render_template, redirect, url_for, flash, request
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance_updater import update_binance_data

import time
import threading

app = Flask(__name__)
app.secret_key = 'qkwdjhd20auwdya28daiufh'

api_key = None
api_secret = None

client = None  # We'll initialize the client once API keys are entered

# Data storage
my_balances = []
open_orders = []

def update_binance_data(client, my_balances, open_orders):
    while True:
        if client:
            try:
                # Update account balance
                account = client.futures_account()
                my_balances.clear()
                my_balances.extend(account['assets'])

                # Update open orders
                open_orders.clear()
                open_orders.extend(client.futures_get_open_orders(symbol=''))

            except BinanceAPIException as e:
                print(f"Error updating data: {e}")
        
        time.sleep(1)  # 1-second interval

# Initialize update thread
update_thread = threading.Thread(target=update_binance_data, args=(client, my_balances, open_orders))
update_thread.daemon = True  # Make sure the thread will exit when the main program exits
update_thread.start()

@app.route("/", methods=['GET', 'POST'])
def index():
    global client
    if request.cookies.get('api_key') and request.cookies.get('api_secret'):
        api_key = request.cookies.get('api_key')
        api_secret = request.cookies.get('api_secret')
        try:
            client = Client(api_key, api_secret)
        except BinanceAPIException:
            client = None

    if client is None:
        return redirect(url_for('login'))
    
    title = "Observer Capital Terminal"
    account = client.futures_account()
    my_balances = account['assets']
    all_symbols = client.get_all_isolated_margin_symbols()
    symbols = [symbol for symbol in all_symbols if symbol['symbol'].endswith(('USDT'))]
    open_orders = client.futures_get_open_orders(symbol='')
    return render_template('index.html', title=title, my_balances=my_balances, open_orders=open_orders, symbols=symbols)

@app.route("/login", methods=['GET', 'POST'])
def login():
    global client
    if request.method == 'POST':
        api_key = request.form['api_key']
        api_secret = request.form['api_secret']

        if not api_key or not api_secret:
            flash("Please provide both API Key and API Secret.", "danger")
            return redirect(url_for('login'))

        try:
            client = Client(api_key, api_secret)
            
            # Set cookies to store API keys
            response = make_response(redirect(url_for('index')))
            response.set_cookie('api_key', api_key)
            response.set_cookie('api_secret', api_secret)
            return response
        except BinanceAPIException as e:
            flash(f"Invalid API keys: {e.message}", "danger")
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route("/logout", methods=['POST'])
def logout():
    global client, api_key, api_secret
    client = None
    api_key = None
    api_secret = None
    
    # Clear cookies
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('api_key')
    response.delete_cookie('api_secret')
    flash("Logged out successfully.", "success")
    return response

@app.route('/buy', methods=['POST'])
def buy():
    global client
    if client is None:
        return redirect(url_for('login'))
    try:
        quantity_str = request.form['quantity']
        symbol = request.form['symbol']
        leverage = int(request.form['leverage'])
        price_str = request.form['price']

        if not quantity_str or not quantity_str.strip():
            flash("Please enter a valid quantity.", "danger")
            return redirect(url_for('index'))

        quantity = float(quantity_str)
        client.futures_change_leverage(symbol=symbol, leverage=leverage)

        # price check, if user leaves it empty it uses market price instead. hopefully lmfao
        if price_str and price_str.strip():
            order_type = Client.ORDER_TYPE_LIMIT
            price = float(price_str)
        else:
            order_type = Client.ORDER_TYPE_MARKET
            price = None

        order = client.futures_create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=order_type,
            timeInForce=Client.TIME_IN_FORCE_GTC if order_type == Client.ORDER_TYPE_LIMIT else None,
            quantity=quantity,
            price=price)

        order_info = f"Symbol: {order['symbol']}, Side: {order['side']}, Quantity: {order['origQty']}, Price: {order.get('price', 'Market Price')}"
        
        flash(f'Order created: {order_info}', 'success')
        
        return redirect(url_for('index'))


    except BinanceAPIException as e:
        if e.code == -4164:
            flash("The total order value must be greater than the minimum requirement. Please adjust your order.", "danger")
        else:
            flash(f"An error occurred: {e.message}", "danger")
        return redirect(url_for('index'))

    except ValueError:
        # Handle conversion errors
        flash("Please enter valid inputs.", "danger")
        return redirect(url_for('index'))
    except Exception as e:
        # General error handling
        print(f"An error occurred: {e}")
        flash("An error occurred while placing the order. Please check your inputs.", "danger")
        return redirect(url_for('index'))


@app.route('/sell', methods=['POST'])
def sell():
    global client
    if client is None:
        return redirect(url_for('login'))
    try:
        quantity_str = request.form['quantity']
        symbol = request.form['symbol']
        leverage = int(request.form['leverage'])
        price_str = request.form['price']

        if not quantity_str or not quantity_str.strip():
            flash("Please enter a valid quantity.", "danger")
            return redirect(url_for('index'))

        quantity = float(quantity_str)
        client.futures_change_leverage(symbol=symbol, leverage=leverage)

        if price_str and price_str.strip():
            order_type = Client.ORDER_TYPE_LIMIT
            price = float(price_str)
        else:
            order_type = Client.ORDER_TYPE_MARKET
            price = None

        order = client.futures_create_order(
            symbol=symbol,
            side=Client.SIDE_SELL,  # This is the line that changes
            type=order_type,
            timeInForce=Client.TIME_IN_FORCE_GTC if order_type == Client.ORDER_TYPE_LIMIT else None,
            quantity=quantity,
            price=price)

        order_info = f"Symbol: {order['symbol']}, Side: {order['side']}, Quantity: {order['origQty']}, Price: {order.get('price', 'Market Price')}"
        
        flash(f'Order created: {order_info}', 'success')
        
        return redirect(url_for('index'))

    except BinanceAPIException as e:
        if e.code == -4164:
            flash("The total order value must be greater than the minimum requirement. Please adjust your order.", "danger")
        else:
            flash(f"An error occurred: {e.message}", "danger")
        return redirect('/')

    except ValueError:
        flash("Please enter valid inputs.", "danger")
        return redirect(url_for('index'))

    except Exception as e:
        print(f"An error occurred: {e}")
        flash("An error occurred while placing the order. Please check your inputs.", "danger")
        return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run()

@app.route('/open_orders')
def open_orders():
    open_orders = client.futures_get_open_orders(symbol='BTCUSDT')
    return 'Open orders: ' + str(open_orders)


@app.route('/settings')
def settings():
    return 'settingstest'