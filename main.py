from config import API_KEY
from loguru import logger
import requests
import telebot
from telebot import types
import datetime as dt


def get_price_coin(coin: str) -> float:
    url = 'https://api.binance.com/api/v3/ticker/price'
    response = requests.get(url, params={'symbol': coin})
    price = float(response.json()['price'])

    return price


bot = telebot.TeleBot(API_KEY)
logger.add('log.txt', format="{time};{level};{message} ")
@bot.message_handler(commands=['start'])  #regexp='[а-яА-я]')
def start(message):
    logger.info(f"{message.from_user.full_name};{message.from_user.id};{message.text}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Bitcoin <-> USD")
    btn2 = types.KeyboardButton("Ethereum <-> USD")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id,
                     text=f"{message.from_user.first_name}, здравствуйте. Курс какой монет интересует)",
                     reply_markup=markup)



@bot.message_handler(content_types=['text'])
def speak(message):
    logger.info(f"{message.from_user.full_name};{message.from_user.id};{message.text}")
    if message.text == "Bitcoin <-> USD":
        bot.send_message(message.from_user.id, f'По состоянию на {dt.datetime.now()} курс: {get_price_coin('BTCUSDT')}')
    if message.text == "Ethereum <-> USD":
        bot.send_message(message.from_user.id, f'По состоянию на {dt.datetime.now()} курс: {get_price_coin("ETHUSDT")}')
    # if message.text.lower() in '0123456789':
    #     # bot.send_message(message.chat.id, 'И все таки пора спать')
    #     bot.send_message(message.chat.id, f'И все таки пора спать. А для информации - твой ID: {message.from_user.id}')
    # elif message.text.lower() in '9876543210':
    #     markup = telebot.types.InlineKeyboardMarkup()
    #     btn1 = telebot.types.InlineKeyboardButton(text='Сайт НБУ', url='https://bank.gov.ua/')
    #     markup.add(btn1)
    #     bot.send_message(message.from_user.id, 'По кнопке ниже можно перейти на сайт НБУ', reply_markup=markup)
    # else:
    #     bot.send_message(message.chat.id, 'Введите любую цифру: ')


bot.polling(non_stop=True)


if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
