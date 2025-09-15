import os , sys , json
import requests
from requests.exceptions import HTTPError , TooManyRedirects , Timeout
from enum import Enum
from decimal import Decimal, getcontext
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction

bsc_api_key = os.environ.get('BINANCE_API_KEY')
secret_key = os.environ.get('BINANCE_SECRET_KEY')
line_secret = os.environ.get('line_secret')
line_channel_token = os.environ.get('line_token')
if not bsc_api_key or not secret_key :
    print('沒找到金鑰')
    sys.exit()

class binance_api(Enum) :
    spot_price = {
        "market" : "spot" ,
        "domain_url" : "https://data-api.binance.vision/api/v3" ,
        "end_point" : "/ticker/price"
    }
    future_price = {
        "market" : "derivative" ,
        "domain_url" : "https://fapi.binance.com" ,
        "end_point" : "/fapi/v2/ticker/price"
    }
    mark_price = {
        "market" : "derivative" ,
        "domain_url" : "https://fapi.binance.com" ,
        "end_point" : "/fapi/v1/premiumIndex"
    }
    funding_rate = {
        "market" : "derivative" ,
        "domain_url" : "https://fapi.binance.com" ,
        "end_point" : "/fapi/v1/fundingRate"
    }

class Binance_data :
    def get_data(self , datatype : binance_api , symbol : str , params : dict = None) -> dict :
        data_info = datatype.value
        domainurl = data_info["domain_url"]
        endpoint = data_info["end_point"]
        ask_url = f"{domainurl}{endpoint}"
        allparams = {"symbol": symbol.upper()}
        if params:
            allparams.update(params)
        try :
            response = requests.get(ask_url , params = params , timeout = 30)
            data = response.json()
            return data
        except requests.exceptions.HTTPError as e:
            print(f"HTTP 錯誤發生： {e}")
            return None
        except TooManyRedirects as e :
            print(f"請求次數過多： {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"請求發生錯誤：{e}")
            return None

if __name__ == "__main__" :
    information = Binance_data()
    choice = {
        1 : binance_api.spot_price ,
        2 : binance_api.future_price ,
        3 : binance_api.mark_price ,
        4 : binance_api.funding_rate
    }
    while True:
        try:
            print('請選擇您想查詢的資料類型:')   
            op = int(input('輸入編號 (1-4)：'))
            if op in choice:
                selected_datatype = choice[op]
                
                symbol = input('輸入想查詢的交易對，如btcusdt').upper()
                
                params = {}
                if selected_datatype == binance_api.funding_rate:
                    params = {"limit": 2}
                
                data = information.get_data(
                    datatype=selected_datatype,
                    symbol=symbol,
                    params=params
                )
                
                if data:
                    print("\n--- 查詢結果 ---")
                    if selected_datatype == binance_api.funding_rate:
                        print(f"幣種: {symbol}")
                        if data:
                            print(f"最新資金費率: {data[0]['fundingRate']}")
                    elif selected_datatype in [binance_api.spot_price, binance_api.future_price]:
                        print(f"幣種: {symbol}")
                        print(f"價格: {data[0]['price']}")
                    elif selected_datatype == binance_api.mark_price:
                        print(f"幣種: {symbol}")
                        print(f"標記價格: {data[0]['markPrice']}")
                else:
                    print("\n無法取得資料，請檢查輸入或稍後再試。")
                continue
            else:
                print('錯誤輸入，請重新輸入1-4之間的數字')
        except ValueError:
            print('錯誤輸入，請重新輸入1-4之間的數字')