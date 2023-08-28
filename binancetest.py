import requests
import json

def test_connectivity():
    response = requests.get("https://api.binance.com/api/v3/ping")
    if response.status_code == 200:
        return "Server is reachable"
    else:
        return "Server is not reachable"

def get_server_time():
    response = requests.get("https://api.binance.com/api/v3/time")
    if response.status_code == 200:
        return json.loads(response.text)["serverTime"]
    else:
        return "Failed to retrieve server time"

def get_exchange_info():
    response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return "Failed to retrieve exchange info"

print(test_connectivity())
print(get_server_time())
print(get_exchange_info())
