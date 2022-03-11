import telebot
import config
import database
import command
import function

from telebot import types

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
            if not function.check_spelling_en(word):
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
            response_message = 'В словарь были добавлены слова, кроме\n\n' + error_mes

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
        word = message_args[1]
        if database.check_repeat_word(message.chat.id, word)[0][0] > 0:
            keyboard = types.InlineKeyboardMarkup()

            del_button = types.InlineKeyboardButton(text='Удалить', callback_data=word)
            keyboard.add(del_button)

            cancel_button = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
            keyboard.add(cancel_button)

            bot.send_message(message.chat.id, 'Вы точно хотите удалить слово ' + word + '?', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Слово не найдено')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    if call.data == 'cancel':
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'accept_btn':
        print('add')
    elif call.data == 'change_btn':
        bot.delete_message(call.message.chat.id, call.message.message_id)

        word = function.get_random_word(call.message.chat.id)
        word_translate = function.google_translate_word(word)

        keyboard = types.InlineKeyboardMarkup()

        accept_btn = types.InlineKeyboardButton(text='Добавить', callback_data='accept_btn')
        keyboard.add(accept_btn)

        change_btn = types.InlineKeyboardButton(text='Поменять', callback_data='change_btn')
        keyboard.add(change_btn)

        bot.send_message(call.message.chat.id, word + ' - ' + word_translate, reply_markup=keyboard)

    else:
        word = call.data
        chat_id = call.message.chat.id

        database.delete_word(chat_id, word)

        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id, 'Слово ' + word + ' удалено из словаря')


@bot.message_handler(commands=["new"])
def start(message):
    word = function.get_random_word(message.chat.id)
    word_translate = function.google_translate_word(word)

    keyboard = types.InlineKeyboardMarkup()

    accept_btn = types.InlineKeyboardButton(text='Добавить', callback_data='accept_btn')
    keyboard.add(accept_btn)

    change_btn = types.InlineKeyboardButton(text='Поменять', callback_data='change_btn')
    keyboard.add(change_btn)

    bot.send_message(message.chat.id, word + ' - ' + word_translate, reply_markup=keyboard)


@bot.message_handler(commands=["test"])
def start(message):
    function.google_translate_word()
    bot.send_message(message.chat.id, 'Test')


@bot.message_handler(commands=["translate"])
def start(message):
    message_args = message.text.split(' ')
    if len(message_args) == 1:
        bot.send_message(message.chat.id, 'Введите слово которое хотите перевести')
    elif len(message_args) > 2:
        bot.send_message(message.chat.id, 'Можно перевести только одно слово')
    else:
        word = message.text.split(' ')[1]
        if function.check_spelling_en(word) or function.check_spelling_ru(word):
            response_message = 'Перевод\n\n' + word + ' - ' + function.google_translate_word(word)
            bot.send_message(message.chat.id, response_message)
        else:
            response_message = "Перевод не возможен \n\n• Проверьте написание слова\n• Перевод доступен с английского " \
                               "и русского"
            bot.send_message(message.chat.id, response_message)


bot.polling(none_stop=True, interval=0)
