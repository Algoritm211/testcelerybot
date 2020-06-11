from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import datetime

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'10',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '4c2aef3a-fc37-4c60-8fc1-297f64af28f0',
}

session = Session()
session.headers.update(headers)


response = session.get(url, params=parameters)
data = json.loads(response.text)

def get_top_10():
    now = datetime.datetime.now()
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    id = 1
    text = '----------\n' + '📍<b>ТОП-10 криптовалют по версии CoinMarketCap</b>📍\n' + '----------\n'
    for elem in data['data']:
        text += '<b>№' + str(id) + '</b> <i>' +elem['name'] + '</i> <code>' + str(round(elem['quote']['USD']['price'], 3)) + '</code> USD ' + \
                str(round(elem['quote']['USD']['percent_change_24h'], 2)) + '(%|24h)\n\n'

        id += 1
    text += '<b>Информация с портала CoinMarketCap по состоянию на ' + now.strftime("%d-%m-%Y") + '</b>'
    return text
