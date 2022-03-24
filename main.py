import telebot
import config
import database
import command
import function

from telebot import types


bot = telebot.TeleBot(config.token)
print('Start bot')


# Команда старта
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привет, ' + message.chat.username + '! Начни изучать слова!')


# Команда добавления в словарь слова от пользователя
@bot.message_handler(commands=["add"])
def start(message):
    args = message.text.split(' ')
    error_word = []

    # checking for arguments
    if len(args) <= 1:
        bot.send_message(message.chat.id,
                         '*Введите слово(-а) которое(-ые) хотите добавить*\n\n'
                         '`/add [word]\n'
                         '/add [word] [word]`',
                         parse_mode="Markdown")
    else:
        words = args
        words.pop(0)

        for word in words:
            word.lower()

            # checking for error
            if not function.check_spelling_en(word):
                error_word.append('_' + word + '_' + ' - слово написано с ошибкой')
            else:
                if database.check_repeat_word(message.chat.id, word)[0][0] > 0:
                    error_word.append('_' + word + '_' + ' - слово уже есть в словаре')
                else:
                    word_translate = function.google_translate_word(word).lower()
                    database.insert_dictionary_db(message.chat.id, word, word_translate)

        error_mes = ''
        for word in error_word:
            error_mes += '• ' + word + '\n'

        if len(error_word) == len(words):
            response_message = '*Слова не были добавлены*\n\n' + error_mes

        else:
            response_message = '*В словарь были добавлены слова, кроме*\n\n' + error_mes

        bot.send_message(message.chat.id, response_message, parse_mode="Markdown")


# Команда вывода словаря пользователя
@bot.message_handler(commands=["dictionary"])
def start(message):
    dictionary_list = command.get_dictionary(message.chat.id)
    message_res = '*Ваш словарь: \n\n№. слово - перевод | процет ответов\n*'

    for word in dictionary_list:
        # word[0] - id / word[1] - word / word[2] - translate / word[3] - statistic of tests
        message_res += str(word[0]) + '. ' + word[1] + ' - ' + word[2] + ' | ' + str(word[3]) + '%\n'

    bot.send_message(message.chat.id, message_res, parse_mode="Markdown")


# Команда удаления слова из словаря пользователя
@bot.message_handler(commands=["delword"])
def start(message):
    message_args = message.text.split(' ')
    if len(message_args) == 1:
        bot.send_message(message.chat.id, '*Введите слово которое хотите удалить*\n\n`/delword [word]`',
                         parse_mode="Markdown")
    else:
        word = message_args[1]
        if database.check_repeat_word(message.chat.id, word)[0][0] > 0:
            keyboard = types.InlineKeyboardMarkup()

            del_button = types.InlineKeyboardButton(text='Удалить', callback_data=word)
            keyboard.add(del_button)

            cancel_button = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
            keyboard.add(cancel_button)

            bot.send_message(message.chat.id, 'Вы точно хотите удалить слово "*' + word + '*"?', reply_markup=keyboard,
                             parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, 'Слово "*' + word + '*" не найдено', parse_mode="Markdown")


def created_btn_new_cmd(message):
    word = function.get_random_word(message.chat.id)
    word_translate = function.google_translate_word(word).lower()

    keyboard = types.InlineKeyboardMarkup()

    accept_btn = types.InlineKeyboardButton(text='Добавить', callback_data='accept_btn')
    keyboard.add(accept_btn)

    change_btn = types.InlineKeyboardButton(text='Поменять', callback_data='change_btn')
    keyboard.add(change_btn)

    bot.send_message(message.chat.id, '*' + word + '* - _' + word_translate + '_', reply_markup=keyboard,
                     parse_mode="Markdown")


# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    if call.data == 'cancel':

        # Обработчик кнопки отмена команды /delword
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == 'accept_btn':

        # Обработчик кнопки принять команды /new
        text = call.message.text
        text_list = text.split(' - ')

        word = text_list[0]
        word_translate = text_list[1]

        database.insert_dictionary_db(call.message.chat.id, word, word_translate)

        bot.delete_message(call.message.chat.id, call.message.message_id)

        bot.send_message(call.message.chat.id, 'Слово "*' + word + '* - _' + word_translate +
                         '_" было добавлено в словарь', parse_mode="Markdown")

    elif call.data == 'change_btn':

        # Обработчик книпки смены слова /new
        bot.delete_message(call.message.chat.id, call.message.message_id)
        created_btn_new_cmd(call.message)

    else:

        # Обработчки кнопки удаления из словаря слова /delword
        word = call.data
        chat_id = call.message.chat.id

        database.delete_word(chat_id, word)

        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id, 'Слово "*' + word + '*" удалено из словаря', parse_mode="Markdown")


# Команда генерации нового слова для изучения
@bot.message_handler(commands=["new"])
def start(message):
    created_btn_new_cmd(message)


# Команда составления теста
@bot.message_handler(commands=["test"])
def start(message):
    bot.send_message(message.chat.id, 'Test')


# Команда для перевода слов
@bot.message_handler(commands=["translate"])
def start(message):
    message_args = message.text.split(' ')

    if len(message_args) == 1:

        bot.send_message(message.chat.id, '*Введите слово которое хотите перевести*\n\n`/translate [word]`\n\n'
                                          '*Доступные переводы:*\n'
                                          '_- C русского на английский\n- С английского на русский_',
                         parse_mode="Markdown")

    elif len(message_args) > 2:

        bot.send_message(message.chat.id, '*Можно перевести только одно слово*\n\n`/translate [word]`\n\n'
                                          '*Доступные переводы:*\n'
                                          '_- C русского на английский\n- С английского на русский_',
                         parse_mode="Markdown")

    else:

        word = message.text.split(' ')[1]

        if function.check_spelling_en(word) or function.check_spelling_ru(word):

            response_message = 'Перевод\n\n*' + word + '* - _' + function.google_translate_word(word) + '_'
            bot.send_message(message.chat.id, response_message, parse_mode="Markdown")
        else:

            response_message = '*Перевод не возможен*\n\n• Проверьте написание слова' \
                               '\n• Перевод доступен с английского и русского'
            bot.send_message(message.chat.id, response_message, parse_mode="Markdown")


bot.polling(none_stop=True, interval=0)
