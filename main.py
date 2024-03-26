from config import API_KEY
from functions import *
from loguru import logger
import requests
import time
import telebot
from telebot import types
import datetime as dt


def get_final_answer_coins(*, coin_name: str) -> str:
    """

    :param coin_name: string name of coin
    :return: string answer of info coin
    """

    date = dt.datetime.today().strftime('%d-%m-%Y %H:%M')
    phrase = (f'на {date}:\n'
              f'{coin_name}\n'
              f'Курс в USDT: {get_price_coin(coin_name=coin_name)[0]}\n'
              f'изменения:\n'
              f'- за 1 час: {get_price_coin(coin_name=coin_name)[1]} %\n'
              f'- за 24 часа: {get_price_coin(coin_name=coin_name)[2]} %\n'
              f'- за 7 дней: {get_price_coin(coin_name=coin_name)[3]} %')

    return phrase


def get_final_answer_rates(*, code: str) -> str:
    """
    func return final frase of answer a rates of choice currency
    :param code: code of currency
    :return: string of answer
    """
    date = dt.datetime.today().strftime('%d-%m-%Y %H:%M')
    phrase = f'на {date}:\n{code}\n'
    # курс НБУ
    phrase += f'Курс НБУ: {get_rate_nbu(valcode=code)[0]}\n'

    # курс монобанка
    if get_rate_mono(valcode=code)[2] is None:
        phrase += f'Курс Монобанка (карты): {get_rate_mono(valcode=code)[0]} - {get_rate_mono(valcode=code)[1]}\n'
    else:
        phrase += f'Курс Монобанка (кросс): {get_rate_mono(valcode=code)[2]}\n'

    # курс приватбанка
    if get_rate_privat_cash(valcode=code) or get_rate_privat_cards(valcode=code):
        phrase += f'Курс Приватбанка (касса): {get_rate_privat_cash(valcode=code)[0]} - {get_rate_privat_cash(valcode=code)[1]}\n'
        phrase += f'Курс Приватбанка (карты): {get_rate_privat_cards(valcode=code)[0]} - {get_rate_privat_cards(valcode=code)[1]}'
    else:
        phrase += f'Курсы Приватбанка отсутствуют'

    return phrase


bot = telebot.TeleBot(API_KEY)
logger.add('log.txt', format="{time};{level};{message} ")


@bot.message_handler(commands=['start'])
def start(message):
    logger.info(f"{message.from_user.full_name};{message.from_user.id};{message.text}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Курсы криптовалют")
    btn2 = types.KeyboardButton("Курсы валют")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id,
                     text=f"<em><b>{message.from_user.first_name}</b>, здравствуйте. Выберите раздел, который Вас интересует</em>",
                     reply_markup=markup, parse_mode='HTML')


@bot.message_handler(context_types=['text'])
def return_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Курсы криптовалют")
    btn2 = types.KeyboardButton("Курсы валют")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id,
                     text=f"<em>Выберите раздел, который Вас интересует</em>", reply_markup=markup, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def speak(message):
    logger.info(f"{message.from_user.full_name};{message.from_user.id};{message.text}")

    # это блок криптовалют
    if message.text == "Курсы криптовалют":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton("BTC")
        btn2 = types.KeyboardButton("ETH")
        btn3 = types.KeyboardButton("TON")
        btn4 = types.KeyboardButton("Возврат в главное меню")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id,
                         text=f"<em><b>{message.from_user.first_name}</b>, курс какой монеты интересует)</em>",
                         reply_markup=markup, parse_mode='HTML')
    elif message.text == "BTC":
        bot.send_message(message.from_user.id, f'{get_final_answer_coins(coin_name="BTC")}')
    elif message.text == "ETH":
        bot.send_message(message.from_user.id, f'{get_final_answer_coins(coin_name="ETH")}')
    elif message.text == "TON":
        bot.send_message(message.from_user.id, f'{get_final_answer_coins(coin_name="TON")}')

    # это блок курсов фиатных валют
    elif message.text == "Курсы валют":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
        btn1 = types.KeyboardButton("🇺🇸 USD")
        btn2 = types.KeyboardButton("🇪🇺 EUR")
        btn3 = types.KeyboardButton("🇨🇦 CAD")
        btn4 = types.KeyboardButton("🇬🇧 GBP")
        btn5 = types.KeyboardButton("Возврат в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.from_user.id,
                         text=f"{message.from_user.first_name}, курс какой валюты интересует)",
                         reply_markup=markup)
    elif message.text == "🇺🇸 USD":
        bot.send_message(message.from_user.id, f'{get_final_answer_rates(code="USD")}')
    elif message.text == "🇪🇺 EUR":
        bot.send_message(message.from_user.id, f'{get_final_answer_rates(code="EUR")}')
    elif message.text == "🇨🇦 CAD":
        bot.send_message(message.from_user.id, f'{get_final_answer_rates(code="CAD")}')
    elif message.text == "🇬🇧 GBP":
        bot.send_message(message.from_user.id, f'{get_final_answer_rates(code="GBP")}')
    elif message.text == "Возврат в главное меню":
        return_main_menu(message)
    else:
        bot.send_message(message.from_user.id, message.text)


@bot.message_handler(content_types=['sticker', 'animation'])
def sticker(message):
    logger.debug(f"{message.from_user.full_name};{message.from_user.id};{message.text}")
    bot.send_message(message.from_user.id, f"Вау! Какая картинка!  ❤️")


if __name__ == '__main__':

    # bot.polling(none_stop=True, interval=2)

    # bot.infinity_polling(timeout=10, long_polling_timeout=5)

    while True:
        try:
            logger.info(f"Bot running..")
            bot.polling(none_stop=True, interval=2)

            # Предполагаю, что бот может мирно завершить работу, поэтому
            # даем выйти из цикла
            break
        except telebot.apihelper.ApiTelegramException as e:
            # requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='api.telegram.org', port=443): Read
            # timed
            # out.(read
            # timeout = 25)
            logger.error(f"Bot has error: {e}")
            bot.stop_polling()

            time.sleep(5)

            logger.info(f"Running again!")