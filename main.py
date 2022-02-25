import telebot

import config
import database
import command

bot = telebot.TeleBot(config.token)
print('Start bot')


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привет, ' + message.chat.username + '! Начни изучать слова!')


@bot.message_handler(commands=["add"])
def start(message):
    message_args = message.text.split(' ')
    if len(message_args) == 1:
        bot.send_message(message.chat.id, 'Введите слово которое хотите добавить')
    else:
        text_message = message.text.split(' ')[1].lower()
        add_result = command.add_word(message.chat.id, text_message)
        bot.send_message(message.chat.id, add_result)


@bot.message_handler(commands=["dictionary"])
def start(message):
    #bot.send_message(message.chat.id, 'Ваш словарь:')
    dictionary_list = command.get_dictionary(message.chat.id)
    message_res = 'Ваш словарь: \n\n'
    message_res += '№. слово - перевод | процет ответов\n'
    for word in dictionary_list:
        message_res += str(word[0]) + '. ' + word[1] + ' - ' + word[2] + ' | ' + str(word[3]) + '%\n'

    bot.send_message(message.chat.id, message_res)


@bot.message_handler(commands=["new"])
def start(message):
    bot.send_message(message.chat.id, 'Какое-то новое слово')


@bot.message_handler(commands=["test"])
def start(message):
    bot.send_message(message.chat.id, 'Test')


@bot.message_handler(commands=["translate"])
def start(message):
    message_args = message.text.split(' ')
    if len(message_args) == 1:
        bot.send_message(message.chat.id, 'Введите слово которое хотите перевести')
    else:
        text_message = message.text.split(' ')[1]
        bot.send_message(message.chat.id, text_message)


bot.polling(none_stop=True, interval=0)
