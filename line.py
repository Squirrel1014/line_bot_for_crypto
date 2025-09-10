import os
import sys
import json , ssl
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

api_key = os.getenv('coinmarket_api_key' , None)
if api_key is None :
    print('尚未設置api金鑰')
    exit(1)

def get_tokenvalue(symbol) :
    domain_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbols' : symbol ,
        'convert' : 'USD'
    }
    headers = {
    'Accept': 'application/json',
    'Accept-Encoding': 'deflate, gzip'
    }
    try :
        response = requests.get(domain_url , param = parameters , headers = headers)
        response.raise_for_status()
        token_price = response.json()
        if price['status']['error_code'] == 0 :
            crypto_data = token_price['data'].get(symbol.upper())
            if crypto_data :
                price = crypto_data['quote']['USD']['price']
                return {
                    "symbol" : 'crypto_data'['symbol'] ,
                    "name" : 'crypto_data'['name'] ,
                    "price" : round(price , 3)
                }
            else :
                print('找不到{symbol}的資料')
                return None
        else:
            print(f"API 請求失敗：{price['status']['error_message']}")
            return None
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(f"網路連線出事啦：{e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 請求有問題哦：{e}")
        return None
    except Exception as e:
        print(f"不知道怎麼了：{e}")
        return None
#測試區
if __name__ == '__main__':
    btc_data = get_tokenvalue('BTC')
    if btc_data:
        print("成功取得 Bitcoin 價格：")
        print(json.dumps(btc_data, indent=4))
    else:
        print("無法取得 Bitcoin 價格。")

    print("\n---")


#目前進度：line官方帳號設定完成，前端尚未設置完成
#要找雲端伺服器部署
#coinmarket api 部署環境變數