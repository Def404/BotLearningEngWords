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
    bot.send_message(message.chat.id, 'Привет, ' + str(message.chat.first_name) + '! Начни изучать слова!')


# Команда добавления в словарь слова от пользователя
@bot.message_handler(commands=["add"])
def start(message):
    args = message.text.split(' ')
    error_word_list = []

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
                error_word_list.append('*• ' + word + '* - слово написано с ошибкой')
            else:
                if database.check_repeat_word(message.chat.id, word)[0][0] > 0:
                    error_word_list.append('*• ' + word + '* - слово уже есть в словаре')
                else:
                    add_words_list.append('*• ' + word + '* - ' + word_translate)
                    database.insert_dictionary_db(message.chat.id, word, word_translate)

        error_mes = ''
        for word in error_word_list:
            error_mes += '• ' + word + '\n'

        if len(error_word_list) == len(words):
            response_message = '*Слово(-а) не было(-и) добавлено(-ы)*\n\n' + error_mes

        elif len(error_word_list) > 0:
            response_message = '*В словарь были добавлены слова, кроме*\n\n' + error_mes

        else:
            response_message = '*Cлово(-а) было(-и) добавлено(-ы)\n\n*'
            for word in add_words_list:
                response_message += word + '\n'

        bot.send_message(message.chat.id, response_message, parse_mode="Markdown")


# Команда вывода словаря пользователя
@bot.message_handler(commands=["dictionary"])
def start(message):
    count = 0
    response_message = '*Ваш словарь: \n\n№. слово - перевод | процент ответов\n*'

    user_db_dict = database.select_dictionary_db(message.chat.id)

    for row in user_db_dict:

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

    bot.send_message(message.chat.id, response_message, parse_mode="Markdown")


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

            del_word_btn = types.InlineKeyboardButton(text='Удалить', callback_data=word)
            keyboard.add(del_word_btn)

            cnl_del_word_btn = types.InlineKeyboardButton(text='Отмена', callback_data='cnl_del_word_btn')
            keyboard.add(cnl_del_word_btn)

            bot.send_message(message.chat.id, 'Вы точно хотите удалить слово "*' + word + '*"?', reply_markup=keyboard,
                             parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, 'Слово "*' + word + '*" не найдено', parse_mode="Markdown")


@bot.message_handler(commands=["deldictionary"])
def start(message):
    keyboard = types.InlineKeyboardMarkup()

    cnl_del_dict_btn = types.InlineKeyboardButton(text='Отмена', callback_data='cnl_del_dict_btn')
    keyboard.add(cnl_del_dict_btn)

    del_dict_btn = types.InlineKeyboardButton(text='Удалить', callback_data='del_dict_btn')
    keyboard.add(del_dict_btn)

    bot.send_message(message.chat.id, 'Вы уверены, что хотите очистить  словарь?\n'
                                      '*Вернуть словарь будет не возможно*',
                     reply_markup=keyboard,
                     parse_mode="Markdown")


def created_btn_new_cmd(message, message_id):
    word = function.get_random_word(message.chat.id)
    word_translate = function.google_translate_word(word).lower()

    keyboard = types.InlineKeyboardMarkup()

    accept_word_btn = types.InlineKeyboardButton(text='Добавить', callback_data='accept_word_btn')
    keyboard.add(accept_word_btn)

    change_word_btn = types.InlineKeyboardButton(text='Поменять', callback_data='change_word_btn ' + str(message_id))
    keyboard.add(change_word_btn)

    cancel_word_btn = types.InlineKeyboardButton(text='Отменить', callback_data='cancel_word_btn ' + str(message_id))
    keyboard.add(cancel_word_btn)

    bot.send_message(message.chat.id, '*' + word + '* - _' + word_translate + '_', reply_markup=keyboard,
                     parse_mode="Markdown")


# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    res = json.loads(call.data)

    if res['key'] == 'next_question':
        questions_id_list = list(res['q_l'])
        question = database.get_word_by_id(questions_id_list[0])[0]

        created_poll(call.message.chat.id, question)

        bot.delete_message(call.message.chat.id, call.message.message_id)

        if len(questions_id_list) > 1:
            questions_id_list.pop(0)
            callback_str = """{"key": "next_question", "q_l": """ + str(questions_id_list) + """}"""
            keyboard = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text='Да', callback_data=callback_str)
            keyboard.add(btn1)
            bot.send_message(call.message.chat.id, 'Следующий вопрос?', reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, 'Тест завершен')

    elif call.data == 'cnl_del_word_btn':

        # Обработчик кнопки отмена команды /delword
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)

    elif call.data == 'accept_word_btn':

        # Обработчик кнопки принять команды /new
        text = call.message.text
        text_list = text.split(' - ')

        word = text_list[0]
        word_translate = text_list[1]

        if database.check_repeat_word(call.message.chat.id, word)[0][0] > 0:
            return

        database.insert_dictionary_db(call.message.chat.id, word, word_translate)

        bot.delete_message(call.message.chat.id, call.message.message_id)

        bot.send_message(call.message.chat.id, 'Слово "*' + word + '* - _' + word_translate +
                         '_" было добавлено в словарь', parse_mode="Markdown")

    elif call.data.split(' ')[0] == 'change_word_btn':

        # Обработчик книпки смены слова /new
        bot.delete_message(call.message.chat.id, call.message.message_id)
        created_btn_new_cmd(call.message, call.data.split(' ')[1])

    elif call.data.split(' ')[0] == 'cancel_word_btn':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.data.split(' ')[1])

    elif call.data == 'cnl_del_dict_btn':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)

    elif call.data == 'del_dict_btn':
        database.del_dict_user(call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'Словарь был очищен')

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
    created_btn_new_cmd(message, message.message_id)


# Команда составления теста
@bot.message_handler(commands=["test"])
def start(message):
    args = message.text.split(' ')
    if len(args) <= 1:
        bot.send_message(message.chat.id, '*Введите кол-во вопросов в тесте (максимум 10)*\n\n'
                                          '`/test [number]`',
                         parse_mode="Markdown")
    else:
        num_question = int(args[1])

        if num_question > database.count_user_dict(message.chat.id):
            bot.send_message(message.chat.id, '*Слов из Вашего словаря не хватает для составления теста*\n\n'
                                              '`Возможное кол-во: ' + str(database.count_user_dict(message.chat.id)) +
                             '` ',
                             parse_mode="Markdown")
        elif num_question > 10:
            bot.send_message(message.chat.id, '*Тест может состоять максимум из 10 вопросов*\n\n',
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
            btn1 = types.InlineKeyboardButton(text='Да', callback_data=callback_str)
            keyboard.add(btn1)
            bot.send_message(message.chat.id, 'Следующий вопрос?', reply_markup=keyboard)


@bot.poll_answer_handler(func=lambda message: True)
def my_poll(message):
    if this_quiz.poll.correct_option_id == message.option_ids[0]:
        question = this_quiz.poll.question
        question_word = question.replace('Как переводтся слово: ', '')
        question_word = question_word.replace('?', '')
        user_id = message.user.id
        database.set_answer(user_id, question_word)


def created_poll(chat_id, question):
    question_str = 'Как переводтся слово: ' + question[2] + '?'

    other_answers = function.get_word_test(database.select_eng_words(), 3)

    other_answer_words = []
    for answer_word in other_answers:
        other_answer_words.append(function.google_translate_word(answer_word[1]))

    other_answer_words.append(question[5])

    random.shuffle(other_answer_words)
    correct_option_id = other_answer_words.index(question[5])
    explanation = 'Правильный ответ: ' + question[5]
    global this_quiz
    this_quiz = bot.send_poll(chat_id=chat_id, question=question_str, options=other_answer_words, type='quiz',
                              correct_option_id=correct_option_id, explanation=explanation, is_anonymous=False)


# Команда для перевода слов
@bot.message_handler(commands=["translate"])
def start(message):
    message_args = message.text.split(' ')

    text = message.text.replace('/translate ', '')
    translate_text = function.google_translate_word(text)
    if len(message_args) == 1:

        response_message = '*Введите слово/фразу которое(-ую) хотите перевести*\n' \
                           '`/translate [word]`\n\n' \
                           '*Доступные переводы:*\n' \
                           '_- C русского на английский\n- С английского на русский_'
    elif len(translate_text) <= 0:

        response_message = '*Перевод не возможен*\n\n• Проверьте написание слова' \
                           '\n• Перевод доступен с английского и русского'
    else:
        response_message = 'Перевод\n\n*' + text + '* - _' + function.google_translate_word(text) + '_'

    bot.send_message(message.chat.id, response_message, parse_mode="Markdown")


bot.polling(none_stop=True, interval=0)
