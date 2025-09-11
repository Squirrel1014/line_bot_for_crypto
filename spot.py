import os
import sys
import json
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from decimal import Decimal, getcontext

#api_key放在本地terminal
bsc_api_key = os.environ.get('BINANCE_API_KEY')
secret_key = os.environ.get('BINANCE_SECRET_KEY')
if not bsc_api_key or not secret_key :
    print('沒找到金鑰')
    sys.exit()

#api 程式碼
def get_token_price(symbol) :
    bsc_url = 'https://data-api.binance.vision/api/v3'
    endpoint = '/ticker/price'
    parameters = {'symbol' : symbol.upper()}
    try :
        response = requests.get(f"{bsc_url}{endpoint}", params=parameters, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = data.get('price')
        return price
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 錯誤發生： {e}")
        return None
    except TooManyRedirects as e :
        print(f"請求次數過多： {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"請求發生錯誤：{e}")
        return None

if __name__ == '__main__':
    while True :
        token_name = input('輸入想要知道的幣種名稱，如btcusdt(必須是一個交易對哦)')
        if token_name.strip().lower() == 'exit':
            print("程式結束。")
            break
        price = get_token_price(token_name)
        if price :
            quantizer = Decimal('0.0001')
            price_decimal = Decimal(price)
            show_price = price_decimal.quantize(quantizer)
            print(f"{token_name}現在價格是：{show_price}")
        else :
            print('f"無法取得{token_name}的價格"')
