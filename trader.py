"""
Suggests what to do with your assets
"""
from pathlib import Path

import json
import requests

def read_last_trade():
    """
    reads last trading price from a file
    """
    home = str(Path.home())
    file_path = home + '/Dropbox/binance/input.json'
    last_trade = None
    with open(file_path) as json_file:
        data = json.load(json_file)
        for trade in data['trades']:
            last_trade = trade

    return last_trade


class Trader():
    """
    main trading class
    """
    def __init__(self):
        self.api_key = ''
        self.api_url = 'https://api.binance.com/api/v3/'

    def avg_price(self):
        """
        get 5m avg price
        """
        price_url = 'avg_price?symbol=BTCUSDT'
        response = requests.get(self.api_url + price_url)
        return response.json()['price']

    def trading_difference(self):
        """
        return difference between current price
        and last traded price
        """
        current_price = self.avg_price()
        history_trade = read_last_trade()
        diff = float(current_price) - history_trade['price']
        return diff, history_trade, current_price

if __name__ == '__main':
    main()

def main():
    """
    main suggestion function
    """
    trade = Trader()
    diff, history_trade, current_price = trade.trading_difference()

    if diff > 100:
        print(current_price + ' is bigger than ' + str(history_trade['price']))
        if history_trade['asset'] == 'BTC':
            print('suggest you to sell BTC')
    elif diff < -100:
        print(current_price + ' is lower than ' +  str(history_trade['price']))
        if history_trade['asset'] == 'USDT':
            print('suggest you to buy BTC')
