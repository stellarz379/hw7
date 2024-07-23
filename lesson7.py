import schedule
import time
import requests

def test():
    print("Helllo Geeks")
    print(time.ctime())

def get_btc_price():
    print("======BTC======")
url = 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
respone = requests.get(url=url).json()
price = respone.get('price')
print(f"Стоимост биткоина в текущее время:{time.ctime()}, Цена:{price}")


