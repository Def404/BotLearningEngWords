import telebot

import config
import database
import command
import function

bot = telebot.TeleBot(config.token)
print('Start bot')


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привет, ' + message.chat.username + '! Начни изучать слова!')


@bot.message_handler(commands=["add"])
def start(message):
    args = message.text.split(' ')
    error_word = []
    response_message = ''

    # checking for arguments
    if len(args) <= 1:
        bot.send_message(message.chat.id, 'Введите слово(-а) которое(-ые) хотите добавить\n\n/add [word]\n/add [word] '
                                          '[word]')
    else:
        words = args
        words.pop(0)

        for word in words:
            word.lower()

            # checking for error
            if not function.check_spelling(word):
                error_word.append(word + ' - слово написано с ошибкой')
            else:
                if database.check_repeat_word(message.chat.id, word)[0][0] > 0:
                    error_word.append(word + ' - слово уже есть в словаре')
                else:
                    database.insert_dictionary_db(message.chat.id, word)

        error_mes = ''
        for word in error_word:
            error_mes += '• ' + word + '\n'

        if len(error_word) == len(words):
            response_message = 'Слова не были добавлены\n\n' + error_mes

        else:
            response_message = 'В словарь были добавлены слова, кроме\n\n'  + error_mes

        bot.send_message(message.chat.id, response_message)


@bot.message_handler(commands=["dictionary"])
def start(message):
    dictionary_list = command.get_dictionary(message.chat.id)
    message_res = 'Ваш словарь: \n\n'
    message_res += '№. слово - перевод | процет ответов\n'
    for word in dictionary_list:
        message_res += str(word[0]) + '. ' + word[1] + ' - ' + word[2] + ' | ' + str(word[3]) + '%\n'

    bot.send_message(message.chat.id, message_res)


@bot.message_handler(commands=["delword"])
def start(message):
    message_args = message.text.split(' ')
    if len(message_args) == 1:
        bot.send_message(message.chat.id, 'Введите слово которое хотите удалить')
    else:
        bot.send_message(message.chat.id, 'sd')


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
        bot.send_message(message.chat.id, command.translate_word(text_message))


bot.polling(none_stop=True, interval=0)
