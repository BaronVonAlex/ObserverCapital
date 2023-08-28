import config, csv
from binance.client import Client

client = Client(config.API_KEY,config.API_SECRET)

ping = client.ping()
time_res = client.get_server_time()
status = client.get_system_status()

print(status,time_res,ping)

candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_5MINUTE)

csvfile = open('12-23_5min_Stick.csv', 'w', newline='')
candlestick_writer = csv.writer(csvfile, delimiter=',')

# for candlestick in candles:
#     print(candlestick)
#     candlestick_writer.writerow(candlestick)
    
# print(len(candles))

candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "1 Jan, 2020", "8 Jul, 2023")
for candlestick in candlesticks:
    candlestick_writer.writerow(candlestick)

csvfile.close()

# prices = client.get_all_tickers()
# for price in prices:
#     print(price)