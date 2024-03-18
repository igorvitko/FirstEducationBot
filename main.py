from config import API_KEY
import requests
import telebot
from bs4 import BeautifulSoup as b

URL = 'https://bank.gov.ua/#4-novyny'

r = requests.get(URL)
# print(r.status_code)
# print(r.text)
soup = b(r.text, 'html.parser')
news = soup.find_all('div', class_='content')
clear_news = [i.text.strip() for i in news]
# for x in clear_news:
#     print(x[])

bot = telebot.TeleBot(API_KEY)
@bot.message_handler(regexp='[а-яА-я]')  # commands=['Привет', 'привет', 'start(']) '
def hello(message):
    bot.send_message(message.chat.id, f"{message.from_user.full_name}, здравствуйте. Пора спать)")


@bot.message_handler(content_types=['text'])
def speak(message):
    if message.text.lower() in '0123456789':
        # bot.send_message(message.chat.id, 'И все таки пора спать')
        bot.send_message(message.chat.id, f'И все таки пора спать. А для информации - твой ID: {message.from_user.id}')
    elif message.text.lower() in '9876543210':
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton(text='Сайт НБУ', url='https://bank.gov.ua/')
        markup.add(btn1)
        bot.send_message(message.from_user.id, 'По кнопке ниже можно перейти на сайт НБУ', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Введите любую цифру: ')

bot.polling()


if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
