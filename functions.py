import requests
from datetime import date

dict_val = {"USD": 840, "EUR": 978, "CAD": 124, "GBP": 826, "PLN": 985}

def get_rate_nbu(valcode: str) -> list[float]:
    date_start = date_end = date.today().strftime('%Y%m%d')
    # dict_val = {840: 'USD', 978: 'EUR', 124: 'CAD'}
    url = (f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={date_start}&end={date_end}&'
           f'valcode={valcode}&sort=exchangedate&order=desc&json')
    response = requests.get(url)
    data = response.json()[0]
    return [data['rate']]


def get_rate_mono(valcode: str) -> list[float]:
    url='https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    answer = response.json()
    for dic in answer:
        if dic['currencyCodeA'] == dict_val[valcode] and dic['currencyCodeB'] == 980:
            rate_buy = dic.get('rateBuy')
            rate_sell = dic.get('rateSell')
            rate_cross = dic.get('rateCross')

    return [rate_buy, rate_sell, rate_cross]


def get_rate_privat_cash(valcode: str) -> list[float]:
    # dict_val = {840: 'USD', 978: 'EUR'}
    url_cash = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response_cash = requests.get(url_cash)
    cash_rate = response_cash.json()
    for item in cash_rate:
        if item['ccy'] == valcode:
            return [item['buy'], item['sale']]


def get_rate_privat_cards(valcode: str) -> list[float]:
    # dict_val = {840: 'USD', 978: 'EUR'}
    url_trans = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    response_trans = requests.get(url_trans)
    trans_rate = response_trans.json()
    for item in trans_rate:
        if item['ccy'] == valcode:
            return [item['buy'], item['sale']]
