import time
import json
import datetime as dt

import requests
from loguru import logger
from telebot import types
from telebot.types import Message

from config import API_KEY, ADMIN_ID, BASE_URL
from functions import *
from my_classses import *

import telebot


def get_final_answer_coins(*, coin_name: str) -> str:
    """
    :param coin_name: string name of coin
    :return: string answer of info coin
    """

    cur_date = dt.datetime.today().strftime('%d-%m-%Y %H:%M:%S')
    price_coin = get_price_coin(coin_name=coin_name)
    phrase = (f'на {cur_date}:\n'
              f'{coin_name}\n'
              f'Курс в USDT: {price_coin[0]}\n'
              f'изменения:\n'
              f'- за 1 час: {price_coin[1]} %\n'
              f'- за 24 часа: {price_coin[2]} %\n'
              f'- за 7 дней: {price_coin[3]} %')

    return phrase


def get_final_answer_rates(*, code: str, message: Message) -> str:
    """
    func return final frase of answer a rates of choice currency
    :param code: code of currency
    :param message: message
    :return: string of answer
    """

    mes_id_del = bot.send_message(message.from_user.id, text="Подождите, формируется ответ....").id

    cur_date = dt.datetime.today().strftime('%d-%m-%Y %H:%M:%S')
    # получаем курсы НБУ
    rate_nbu = get_rate_nbu(valcode=code)
    # получаем курсы монобанка
    rate_mono = get_rate_mono(valcode=code)
    # получаем курсы приватбанка
    rate_privat_cash = get_rate_privat_cash(valcode=code)
    rate_privat_card = get_rate_privat_cards(valcode=code)
    # получаем оптовые курсы обмена
    if code == "USD" or code == "EUR":
        rate_kit = get_rate_wholesale(valcode=code)

    # формируем финальное сообщение
    phrase = f'на {cur_date}:\nКурс валюты {code}:\n'
    # добавляем курс НБУ
    phrase += f'- НБУ: {rate_nbu[0]}\n'
    # добавляем курс монобанка
    if rate_mono[2] is None:
        phrase += f'- Монобанк (карты): {rate_mono[0]} - {rate_mono[1]}\n'
    else:
        phrase += f'- Монобанк (кросс): {rate_mono[2]}\n'
    # добавляем курсы приватбанка
    if rate_privat_cash or rate_privat_card:
        phrase += f'- Приватбанк (касса): {rate_privat_cash[0]} - {rate_privat_cash[1]}\n'
        phrase += f'- Приватбанк (карты): {rate_privat_card[0]} - {rate_privat_card[1]}'
    else:
        phrase += f'Курсы Приватбанка отсутствуют'

    # добавляем оптовые курсы, только для USD и EUR
    if code == "USD" or code == "EUR":
        phrase += f"\n- Оптовый обменник: {rate_kit[0]} - {rate_kit[1]} "

    bot.delete_message(message.chat.id, mes_id_del)

    return phrase


telegram_client = TelegramClient(API_KEY, base_url=BASE_URL)
bot = MyBot(token=API_KEY, telegram_client=telegram_client)

logger.add(logger_path, format="{time};{level};{message} ")


@bot.message_handler(commands=['start'])
def start(message: Message):
    logger.info(f"{message.from_user.full_name};{message.from_user.id};{message.text}")

    with open(users_path, 'r') as f:
        data_from_json = json.load(f)

    user_id = message.from_user.id
    user_name = message.from_user.full_name
    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {"user_name": user_name}

        with open(users_path, 'w') as f:
            json.dump(data_from_json, f, indent=4, ensure_ascii=False)

        bot.reply_to(message=message, text=f"{user_name}, Вы зарегистрированы!\n"
                                       f"Ваш user_id: {user_id}")

        logger.info(f"User {user_name};{user_id}; was registrated!")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Курсы криптовалют")
    btn2 = types.KeyboardButton("Курсы валют")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id,
                     text=f"<em><b>{message.from_user.first_name}</b>, здравствуйте. Выберите раздел, "
                          f"который Вас интересует</em>",
                     reply_markup=markup, parse_mode='HTML')

@bot.message_handler(commands=["help"])
def help_content(message: Message):
    bot.send_message(message.from_user.id, text="Это бот умеет искать и предоставлять информацию.\n\n"
                                                "1. Курсы валют от банков:\n"
                                                "НБУ https://bank.gov.ua/ua/markets/exchangerates,\n"
                                                "Монобанка https://www.monobank.ua/?lang=uk,\n"
                                                "Приватбанка https://privatbank.ua/ \n\n"
                                                "2. Котировки некоторых монет "
                                                "криптовалют от CoinLore https://www.coinlore.com/", disable_web_page_preview=True)


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
        bot.send_message(message.from_user.id, f'{get_final_answer_rates(code="USD", message=message)}')
    elif message.text == "🇪🇺 EUR":
        bot.send_message(message.from_user.id, f'{get_final_answer_rates(code="EUR", message=message)}')
    elif message.text == "🇨🇦 CAD":
        bot.send_message(message.from_user.id, f'{get_final_answer_rates(code="CAD", message=message)}')
    elif message.text == "🇬🇧 GBP":
        bot.send_message(message.from_user.id, f'{get_final_answer_rates(code="GBP", message=message)}')
    elif message.text == "Возврат в главное меню":
        return_main_menu(message)
    else:
        bot.send_message(message.from_user.id, message.text)


@bot.message_handler(content_types=['sticker', 'animation'])
def sticker(message):
    logger.debug(f"{message.from_user.full_name};{message.from_user.id};{message.text}")
    # bot.send_message(message.from_user.id, f"Вау! Какая картинка!  ❤️")
    bot.reply_to(message, f"Вау! Какая картинка!  ❤️")


if __name__ == '__main__':

    # bot.polling(none_stop=True, interval=2)

    # bot.infinity_polling(timeout=10, long_polling_timeout=5)

    def create_err_message(err):
        return f"{dt.datetime.now()}:::\n{err.__class__}:::\n{err}"


    while True:
        try:
            logger.info(f"Bot running..")
            bot.polling(none_stop=True, interval=2)

            # Предполагаю, что бот может мирно завершить работу, поэтому
            # даем выйти из цикла
            break
        # except telebot.apihelper.ApiTelegramException as e:
        except Exception as err:
            # requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='api.telegram.org', port=443):
            # Read timed out.(read timeout = 25)
            logger.error(f"Bot has error: {err.__class__}:::{err}")
            bot.telegram_client.post(method="sendMessage", params={'chat_id': ADMIN_ID,
                                                                 "text": create_err_message(err)})

            # requests.post(f"https://api.telegram.org/bot{API_KEY}/"
            #               f"sendMessage?chat_id=228927462&text={dt.datetime.now()}:::{err.__class__}:::{e}")
            bot.stop_polling()

            time.sleep(5)

            logger.info(f"Running again!")