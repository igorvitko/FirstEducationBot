import requests
import telebot

from config import *
from telebot import TeleBot

class TelegramClient:
    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url

    def prepare_url(self, method: str):
        result_url = f"{self.base_url}/bot{self.token}/"
        if method is not None:
            result_url += method

        return result_url

    def post(self, method: str = None, params: dict = None, body: dict = None):
        url = self.prepare_url(method)
        response = requests.post(url, params=params, data=body)

        return response


class MyBot(telebot.TeleBot):
    def __init__(self, telegram_client: TelegramClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telegram_client = telegram_client




if __name__ == "__main__":
    pass

    # base_url = "https://api.telegram.org"
    # my_bot = TelegramClient(token=API_KEY, base_url=base_url)
    # my_params = {"chat_id": 228927462, "text": "helloOOOO world"}
    # print(my_bot.post(method='sendMessage', params=my_params).json())

#     telegram_client = TelegramClient(API_KEY, base_url)
#     bot = MyBot(token=API_KEY, telegram_client=telegram_client)
#
#     print(bot.telegram_client.post(method="sendMessage", params=my_params))
#     chat_id=228927462&text={dt.datetime.now()}:::{err.__class__}:::{e}"