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

def get_rate_of_currency(currency: str) -> float:
    pass


bot = telebot.TeleBot(API_KEY)
logger.add('log.txt', format="{time};{level};{message} ")
@bot.message_handler(commands=['start'])  #regexp='[а-яА-я]')
def start(message):
    logger.info(f"{message.from_user.full_name};{message.from_user.id};{message.text}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Курсы криптовалют")
    btn2 = types.KeyboardButton("Курсы НБУ")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id,
                     text=f"<em><b>{message.from_user.first_name}</b>, здравствуйте. Выберите раздел, который Вас интересует</em>",
                     reply_markup=markup, parse_mode='HTML')


@bot.message_handler(context_types=['text'])
def return_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Курсы криптовалют")
    btn2 = types.KeyboardButton("Курсы НБУ")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id,
                     text=f"<em>Выберите раздел, который Вас интересует</em>", reply_markup=markup, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def speak(message):
    logger.info(f"{message.from_user.full_name};{message.from_user.id};{message.text}")
    if message.text == "Курсы криптовалют":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("Bitcoin <-> USD")
        btn2 = types.KeyboardButton("Ethereum <-> USD")
        btn3 = types.KeyboardButton("Возврат в главное меню")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id,
                         text=f"<em><b>{message.from_user.first_name}</b>, курс какой монеты интересует)</em>",
                         reply_markup=markup, parse_mode='HTML')
    elif message.text == "Bitcoin <-> USD":
        bot.send_message(message.from_user.id, f'По состоянию на {dt.datetime.now()} курс: {get_price_coin('BTCUSDT')}')
    elif message.text == "Ethereum <-> USD":
        bot.send_message(message.from_user.id, f'По состоянию на {dt.datetime.now()} курс: {get_price_coin("ETHUSDT")}')
    elif message.text == "Курсы НБУ":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
        btn1 = types.KeyboardButton("USD")
        btn2 = types.KeyboardButton("EUR")
        btn3 = types.KeyboardButton("CAD")
        btn4 = types.KeyboardButton("PLN")
        btn5 = types.KeyboardButton("Возврат в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.from_user.id,
                         text=f"{message.from_user.first_name}, курс какой валюты интересует)",
                         reply_markup=markup)
    elif message.text == "Курс USD":
        bot.send_message(message.from_user.id, f'Раздел в разработке... Скоро будет')
    elif message.text == "Курс EUR":
        bot.send_message(message.from_user.id, f'Раздел в разработке... Скоро будет')
    elif message.text == "Возврат в главное меню":
        return_main_menu(message)
    else:
        bot.send_message(message.from_user.id, message.text)
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


@bot.message_handler(content_types=['sticker', 'animation'])
def sticker(message):
    logger.debug(f"{message.from_user.full_name};{message.from_user.id};{message.text}")
    bot.send_message(message.from_user.id, f"Вау! Какая картинка!")



# bot.polling(non_stop=True)

if __name__ == '__main__':
    bot.polling(non_stop=True)