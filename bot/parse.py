import requests

def get_crypto_to_usdt(crypto):
    to_url = crypto.upper()
    url_usdt = 'https://api.binance.com/api/v3/ticker/price?symbol={}USDT'.format(to_url)
    resp_usdt = requests.get(url_usdt).json()
    if 'code' in resp_usdt:
        return '❌' + to_url + ' не торгуется против USDT на Binance❌\n'
    else:
        price_usdt = resp_usdt['price']
        return '<code>' + str(price_usdt) + '</code>' + ' USDT\n'


def get_crypto_to_btc(crypto):
    to_url = crypto.upper()
    url_btc = 'https://api.binance.com/api/v3/ticker/price?symbol={}BTC'.format(to_url)
    resp_btc = requests.get(url_btc).json()
    if 'code' in resp_btc:
        return '❌' + to_url + ' не торгуется против BTC на Binance❌\n'
    else:
        price_btc = resp_btc['price']
    return '<code>' + str(price_btc) + '</code>' + ' BTC\n'
