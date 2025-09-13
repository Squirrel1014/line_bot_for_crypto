import os
import json
import sys
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from decimal import Decimal, getcontext

def get_futures_price(symbol) :
    bsc_url = 'https://fapi.binance.com'
    end_point = '/fapi/v1/ticker/24hr'
    parameters = {'symbol' : symbol.upper()}
    try :
        response = requests.get(f"{bsc_url}{end_point}" , params = parameters , timeout = 10)
        response.raise_for_status()
        data = response.json()
        last_price = data.get('lastPrice')
        return last_price
    except requests.exceptions.HTTPError as e:
        print('HTTP 發生錯誤')
        print(f'錯誤狀態碼: {e.response.status_code}')
        print(f'錯誤訊息: {e}')
        return None
    except requests.exceptions.ConnectionError as e :
        print('連結錯誤')
        return None
    except TooManyRedirects as e :
        print('多次請求未能成功')
        return None

if __name__ == '__main__' :
    while True :
        token_name = input('輸入想查詢的代幣交易對，如btcusdt')
        if token_name.lower().strip() == 'exit' :
            break
        if token_name :
            symbol = token_name.strip()
            price = get_futures_price(symbol)
        if price :
            quantizer = Decimal('0.0001')
            price_decimal = Decimal(price)
            show_price = price_decimal.quantize(quantizer)
            print(f"{token_name}現在價格是：{show_price}")
        else :
            print('f"無法取得{token_name}的價格"')

