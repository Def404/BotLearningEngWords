import telebot

import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')


@bot.message_handler(commands=["test"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'test')


@bot.message_handler(commands=["add"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'add')


def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


bot.polling(none_stop=True, interval=0)
