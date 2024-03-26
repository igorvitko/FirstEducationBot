from config import API_KEY
from functions import *
from loguru import logger
import requests
import time
import telebot
from telebot import types
import datetime as dt


def get_price_coin(coin):
    url = 'https://api.coinlore.net/api/ticker/'
    response = requests.get(url, params={'id': coin})
    price = response.json()[0]['price_usd']
    price_change_24h = response.json()[0]['percent_change_24h']

    return price, price_change_24h

dict_val = {"USD": 840, "EUR": 978, "CAD": 124, "GBP": 826, "PLN": 985}


def get_final_answer_rates(*, code: str) -> str:
    """
    func return final frase of answer a rates of choice currency
    :param code: choice currency
    :return: string of answer
    """
    date = dt.datetime.today().strftime('%d-%m-%Y %H:%M')
    phrase = f'на {date}:\n\n'
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("Bitcoin <-> USD")
        btn2 = types.KeyboardButton("Ethereum <-> USD")
        btn3 = types.KeyboardButton("Возврат в главное меню")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id,
                         text=f"<em><b>{message.from_user.first_name}</b>, курс какой монеты интересует)</em>",
                         reply_markup=markup, parse_mode='HTML')
    elif message.text == "Bitcoin <-> USD":
        bot.send_message(message.from_user.id, f"По состоянию на {dt.datetime.now()} \n "
                                               f"курс: <b>{get_price_coin(90)[0]}</b>, "
                                               f"измен. за 24 часа <b>{get_price_coin(90)[1]}</b>% ", parse_mode='HTML')
    elif message.text == "Ethereum <-> USD":
        bot.send_message(message.from_user.id, f"По состоянию на {dt.datetime.now()} \n "
                                               f"курс: <b>{get_price_coin(80)[0]}</b>, "
                                               f"измен. за 24 часа <b>{get_price_coin(80)[1]}</b> %", parse_mode='HTML')

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
        bot.send_message(message.from_user.id, f'{get_final_answer_rates(code='USD')}')
    elif message.text == "🇪🇺 EUR":
        bot.send_message(message.from_user.id, f'{get_final_answer_rates(code='EUR')}')
    elif message.text == "🇨🇦 CAD":
        bot.send_message(message.from_user.id, f'{get_final_answer_rates(code='CAD')}')
    elif message.text == "🇬🇧 GBP":
        bot.send_message(message.from_user.id, f'{get_final_answer_rates(code='CAD')}')
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
    bot.send_message(message.from_user.id, f"Вау! Какая картинка!  ❤️")


if __name__ == '__main__':
    # bot.polling(none_stop=True, interval=2)
    while True:
        try:
            logger.info(f"Bot running..")
            bot.polling(none_stop=True, interval=2)

            # Предполагаю, что бот может мирно завершить работу, поэтому
            # даем выйти из цикла
            break
        except telebot.apihelper.ApiException as e:
            logger.error(f"Bot has error: {e}")
            bot.stop_polling()

            time.sleep(5)

            logger.info(f"Running again!")