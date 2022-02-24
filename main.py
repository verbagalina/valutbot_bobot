import telebot
from telebot import types
from config import Token, money
from api import APIexception, Convert


bot = telebot.TeleBot(Token)

@bot.message_handler(commands = ["start", "help"]) #приветствие
def start(message: types.Message):
    p = "Приветствую! \n" \
        "Введите в одну строчку через пробел: \n- имя валюты, цену которой вы хотите узнать в именительном падеже единственном числе. \n" \
        "- имя валюты, в которой надо узнать ценну первой валюты в именительном падеже единственном числе. \n" \
        "- количество первой валюты в числовом формате."

    bot.send_message(message.chat.id, p)

@bot.message_handler(commands = ["values"]) #доступные валюты
def values(message: types.Message):
    v = "Доступна информация о следующих валютах:\n "
    for i in money.keys():
        v += "- " + i +"\n"
    bot.reply_to(message, v)

@bot.message_handler(content_types = ["text"])#обработка команд пользователя
def convert(message: types.Message):
    q = message.text.split()
    try:
        if len(q) != 3:
            raise APIexception("Вы ввели неверное количество параметров.")
        if not q[2].isdigit():
            raise APIexception("Вы не ввели количество первой валюты.")
        if (q[0].lower() not in money.keys()) or (q[1].lower() not in money.keys()):
            raise APIexception("Вы ввели валюту, информация о которой недоступна.")
        if q[0].lower() == q[1].lower():
            raise APIexception("Вы ввели одинаковые валюты.")
    except APIexception as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, f"Возникла неизвестная ошибка: {e}")
    else:
        bot.reply_to(message, f"Цена {q[2]} {q[0]} в {q[1]} - {Convert.get_price(q[0].lower(), q[1].lower(), q[2])}")



bot.polling()