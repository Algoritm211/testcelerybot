from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import datetime

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD',
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '4c2aef3a-fc37-4c60-8fc1-297f64af28f0',
}

session = Session()
session.headers.update(headers)



response = session.get(url, params=parameters)

def get_data():
    data = json.loads(response.text)
    return data
