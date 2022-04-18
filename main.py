import random
import telebot
import config
import database
import function
import re
import json

from telebot import types

bot = telebot.TeleBot(config.token)
print('Start bot')


# Команда старта
@bot.message_handler(commands=["start"])
def start(message):
    message_text = 'Привет, *' + str(message.chat.first_name) + '*!\n'
    message_text += 'Данный бот позволит Вам изучить английские слова!\n\n' \
                    'Вы сможете хранить все изученые слова в одном месте\n' \
                    'Пройти тест на знание изученных слов\n' \
                    'Переводить слова и фразы\n\n' \
                    '*Команды:*\n' \
                    '`/new - изучить новое слово\n' \
                    '/add [слово] - добавть слово в словарь\n' \
                    '/add [слово] [слово] - добавить несколько слов в словарь\n' \
                    '/dictionary - Ваш словарь\n' \
                    '/test [количество вопросов] - пройти тест на изучение слов (максимум 10 вопросов)\n' \
                    '/translate [слово/фраза] - перевод слов и фраз  (С английского на русский; С русского на английский)\n' \
                    '/delword [слово] - удалить слово из словаря\n' \
                    '/deldictionary - очистить словарь\n' \
                    '/info | /help - информация о боте`\n\n' \
                    'Разработчик: @adef15'
    bot.send_message(message.chat.id,
                     message_text,
                     parse_mode="Markdown")


# Команда добавления в словарь слова от пользователя
@bot.message_handler(commands=["add"])
def add(message):
    args = message.text.split(' ')
    error_words_list = []

    # checking for arguments
    if len(args) <= 1:
        message_text = '*Введите слово(-а) которое(-ые) хотите добавить*\n\n' \
                       '`/add [word]\n' \
                       '/add [word] [word]`'

        bot.send_message(message.chat.id,
                         message_text,
                         parse_mode="Markdown")
    else:
        words = args
        words.pop(0)

        add_words_list = []

        for word in words:

            word.lower()

            word = re.sub("[.|.|?]", "", word)

            word_translate = function.google_translate_word(word).lower()

            # checking for error
            if not function.check_spelling_en(word) or \
                    re.sub("[0-9]", "", word) == "" or \
                    len(word) < 2 or \
                    len(word_translate) <= 0:

                error_words_list.append('* ' + word + '* - слово написано с ошибкой')
            else:
                if database.check_repeat_word(message.chat.id, word) > 0:
                    error_words_list.append('* ' + word + '* - слово уже есть в словаре')
                else:
                    add_words_list.append('* ' + word + '* - ' + word_translate)
                    database.set_user_word(message.chat.id, word, word_translate)

        error_message = ''
        for word in error_words_list:
            error_message += '• ' + word + '\n'

        if len(error_words_list) == len(words):
            response_message = '*Слово(-а) не было(-и) добавлено(-ы)*\n\n' + error_message

        elif len(error_words_list) > 0:
            response_message = '*В словарь были добавлены слова, кроме*\n\n' + error_message

        else:
            response_message = '*Cлово(-а) было(-и) добавлено(-ы)\n\n*'
            for word in add_words_list:
                response_message += word + '\n'

        bot.send_message(message.chat.id,
                         response_message,
                         parse_mode="Markdown")


# Команда вывода словаря пользователя
@bot.message_handler(commands=["dictionary"])
def dictionary(message):
    count = 0
    response_message = '*Ваш словарь: \n\n№. слово - перевод | процент ответов\n*'

    words_user_list = database.get_user_dict(message.chat.id)

    for row in words_user_list:

        result_test = 0
        count += 1

        word = row[2]
        translate_word = row[5]

        # row[3] - кол-во раз попав в тесте
        # row[4] - кол-во раз ответ в тесте
        if row[3] != 0:
            result_test = row[4] / row[3] * 100
            result_test = round(result_test, 1)

        response_message += str(count) + '. ' + word + ' - ' + translate_word + ' | _' + str(result_test) + '%_\n'

    bot.send_message(message.chat.id,
                     response_message,
                     parse_mode="Markdown")


# Команда удаления слова из словаря пользователя
@bot.message_handler(commands=["delword"])
def delword(message):
    message_args = message.text.split(' ')
    if len(message_args) == 1:
        message_text = '*Введите слово которое хотите удалить*\n\n' \
                       '`/delword [word]`'
        bot.send_message(message.chat.id,
                         message_text,
                         parse_mode="Markdown")
    else:
        del_word = message_args[1]

        if database.check_repeat_word(message.chat.id, del_word) > 0:

            keyboard = types.InlineKeyboardMarkup()
            del_word_str = '"' + del_word + '"'

            callback_del_str = """{"key": "del_word_btn", "word_text": """ + del_word_str + """}"""
            del_word_btn = types.InlineKeyboardButton(text='Удалить', callback_data=callback_del_str)
            keyboard.add(del_word_btn)

            callback_cnl_str = """{"key": "cnl_del_word"}"""
            cnl_del_word_btn = types.InlineKeyboardButton(text='Отмена', callback_data=callback_cnl_str)
            keyboard.add(cnl_del_word_btn)

            message_text = 'Вы точно хотите удалить слово "*' + del_word + '*"?'

            bot.send_message(message.chat.id,
                             message_text,
                             reply_markup=keyboard,
                             parse_mode="Markdown")
        else:

            message_text = 'Слово "*' + del_word + '*" не найдено'
            bot.send_message(message.chat.id,
                             message_text,
                             parse_mode="Markdown")


@bot.message_handler(commands=["deldictionary"])
def deldictionary(message):
    keyboard = types.InlineKeyboardMarkup()

    callback_del_str = """{"key": "del_dict"}"""
    del_dict_btn = types.InlineKeyboardButton(text='Удалить',
                                              callback_data=callback_del_str)
    keyboard.add(del_dict_btn)

    callback_cnl_str = """{"key": "cnl_del_dict"}"""
    cnl_del_dict_btn = types.InlineKeyboardButton(text='Отмена',
                                                  callback_data=callback_cnl_str)
    keyboard.add(cnl_del_dict_btn)

    message_text = 'Вы уверены, что хотите очистить  словарь?\n' \
                   '*Вернуть словарь будет не возможно*'

    bot.send_message(message.chat.id,
                     message_text,
                     reply_markup=keyboard,
                     parse_mode="Markdown")


# Команда генерации нового слова для изучения
@bot.message_handler(commands=["new"])
def new(message):
    created_btn_new_cmd(message, message.message_id)


def created_btn_new_cmd(message, message_id):

    new_word = function.get_random_word(message.chat.id)
    new_word_translate = function.google_translate_word(new_word).lower()

    keyboard = types.InlineKeyboardMarkup()

    callback_acc_str = """{"key": "accept_new_word"}"""
    accept_word_btn = types.InlineKeyboardButton(text='Добавить',
                                                 callback_data=callback_acc_str)
    keyboard.add(accept_word_btn)

    callback_chg_str = """{"key": "change_new_word", "message_id": """ + str(message_id) + """}"""
    change_word_btn = types.InlineKeyboardButton(text='Поменять',
                                                 callback_data=callback_chg_str)
    keyboard.add(change_word_btn)

    callback_cnl_str = """{"key": "cancel_new_word", "message_id": """ + str(message_id) + """}"""
    cancel_word_btn = types.InlineKeyboardButton(text='Отменить',
                                                 callback_data=callback_cnl_str)
    keyboard.add(cancel_word_btn)

    message_text = '*' + new_word + '* - _' + new_word_translate + '_'

    bot.send_message(message.chat.id,
                     message_text,
                     reply_markup=keyboard,
                     parse_mode="Markdown")


# Команда для перевода слов
@bot.message_handler(commands=["translate"])
def translate(message):
    message_args = message.text.split(' ')

    text_for_translate = message.text.replace('/translate ', '')
    translate_text = function.google_translate_word(text_for_translate)
    if len(message_args) == 1:

        response_message = '*Введите слово/фразу которое(-ую) хотите перевести*\n' \
                           '`/translate [word]`\n\n' \
                           '*Доступные переводы:*\n' \
                           '_- C русского на английский\n' \
                           '- С английского на русский_'
    elif len(translate_text) <= 0:

        response_message = '*Перевод не возможен*\n\n' \
                           '• Проверьте написание слова\n' \
                           '• Перевод доступен с английского и русского'
    else:
        response_message = 'Перевод\n\n' \
                           '*' + text_for_translate + '* - _' + translate_text + '_'

    bot.send_message(message.chat.id,
                     response_message,
                     parse_mode="Markdown")

@bot.message_handler(commands=["info", "help"])
def help(message):
    message_text = 'Данный бот позволит Вам изучить английские слова!\n\n' \
                    'Вы сможете хранить все изученые слова в одном месте\n' \
                    'Пройти тест на знание изученных слов\n' \
                    'Переводить слова и фразы\n\n' \
                    '*Команды:*\n' \
                    '`/new - изучить новое слово\n' \
                    '/add [слово] - добавть слово в словарь\n' \
                    '/add [слово] [слово] - добавить несколько слов в словарь\n' \
                    '/dictionary - Ваш словарь\n' \
                    '/test [количество вопросов] - пройти тест на изучение слов (максимум 10 вопросов)\n' \
                    '/translate [слово/фраза] - перевод слов и фраз  (С английского на русский; С русского на английский)\n' \
                    '/delword [слово] - удалить слово из словаря\n' \
                    '/deldictionary - очистить словарь\n' \
                    '/info | /help - информация о боте`\n\n' \
                    'Разработчик: @adef15'
    bot.send_message(message.chat.id,
                     message_text,
                     parse_mode="Markdown")


# Команда составления теста
@bot.message_handler(commands=["test"])
def test(message):
    args = message.text.split(' ')
    if len(args) <= 1:
        message_text = '*Введите кол-во вопросов в тесте (максимум 10)*\n\n' \
                       '`/test [number]`'

        bot.send_message(message.chat.id,
                         message_text,
                         parse_mode="Markdown")
    else:
        num_question = int(args[1])

        count_words_user = database.count_user_words(message.chat.id)

        if num_question > count_words_user:

            message_text = '*Слов из Вашего словаря не хватает для составления теста*\n\n' \
                           '`Возможное кол-во: ' + str(count_words_user) + '` '

            bot.send_message(message.chat.id,
                             message_text,
                             parse_mode="Markdown")

        elif num_question > 10:
            message_text = '*Тест может состоять максимум из 10 вопросов*'

            bot.send_message(message.chat.id,
                             message_text,
                             parse_mode="Markdown")
        else:
            questions_list = function.get_test(message.chat.id, num_question)

            question_1st = questions_list[0]
            created_poll(message.chat.id, question_1st)

            questions_id_list = []

            for question in questions_list:
                questions_id_list.append(question[0])

            questions_id_list.pop(0)

            callback_str = """{"key": "next_question", "q_l": """ + str(questions_id_list) + """}"""

            keyboard = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text='Да',
                                              callback_data=callback_str)
            keyboard.add(btn1)

            bot.send_message(message.chat.id,
                             'Следующий вопрос?',
                             reply_markup=keyboard)


def created_poll(chat_id, question):
    question_str = 'Как переводтся слово: ' + question[2] + '?'

    other_answers = function.get_word_test(database.get_eng_words(), 3)

    other_answer_words = []
    for answer_word in other_answers:
        other_answer_words.append(function.google_translate_word(answer_word[0]))

    other_answer_words.append(question[5])

    random.shuffle(other_answer_words)
    correct_option_id = other_answer_words.index(question[5])
    explanation = 'Правильный ответ: ' + question[5]

    global this_quiz
    this_quiz = bot.send_poll(chat_id=chat_id,
                              question=question_str,
                              options=other_answer_words,
                              type='quiz',
                              correct_option_id=correct_option_id,
                              explanation=explanation,
                              is_anonymous=False)


@bot.poll_answer_handler(func=lambda message: True)
def my_poll(message):
    if this_quiz.poll.correct_option_id == message.option_ids[0]:

        question_word = this_quiz.poll.question.replace('Как переводтся слово: ', '').replace('?', '')
        user_id = message.user.id

        database.set_answer_word(user_id, question_word)


# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    callback = json.loads(call.data)

    if callback['key'] == 'next_question':
        questions_id_list = list(callback['q_l'])
        question = database.get_word_by_id(questions_id_list[0])[0]

        created_poll(call.message.chat.id, question)

        bot.delete_message(call.message.chat.id, call.message.message_id)

        if len(questions_id_list) > 1:

            questions_id_list.pop(0)

            callback_str = """{"key": "next_question", "q_l": """ + str(questions_id_list) + """}"""

            keyboard = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text='Да',
                                              callback_data=callback_str)
            keyboard.add(btn1)

            bot.send_message(call.message.chat.id,
                             'Следующий вопрос?',
                             reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id,
                             'Тест завершен')

    elif callback['key'] == 'del_word_btn':
        print(callback['word_text'])
        del_word = callback['word_text']
        chat_id = call.message.chat.id

        database.delete_word(chat_id, del_word)

        bot.delete_message(chat_id, call.message.message_id)

        message_text = 'Слово "*' + del_word + '*" удалено из словаря'
        bot.send_message(chat_id,
                         message_text,
                         parse_mode="Markdown")

    elif callback['key'] == 'cnl_del_word':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)

    elif callback['key'] == 'accept_new_word':
        text = call.message.text
        text_list = text.split(' - ')

        word = text_list[0]
        word_translate = text_list[1]

        if database.check_repeat_word(call.message.chat.id, word) > 0:
            return

        database.set_user_word(call.message.chat.id, word, word_translate)

        bot.delete_message(call.message.chat.id, call.message.message_id)

        message_text = 'Слово "*' + word + '* - _' + word_translate + '_" было добавлено в словарь'
        bot.send_message(call.message.chat.id,
                         message_text,
                         parse_mode="Markdown")

    elif callback['key'] == 'change_new_word':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        created_btn_new_cmd(call.message, callback['message_id'])

    elif callback['key'] == 'cancel_new_word':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, callback['message_id'])

    elif callback['key'] == 'cnl_del_dict':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)

    elif callback['key'] == 'del_dict':
        database.del_dict_user(call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'Словарь был очищен')


bot.polling(none_stop=True, interval=0)
