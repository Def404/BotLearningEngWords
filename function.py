import enchant
from googletrans import Translator
import random
import database


# Фун-ия проверки правописания на английском
def check_spelling_en(word):
    dictionary = enchant.Dict('en_US')
    check_result = dictionary.check(word)
    return check_result


# Фун-ия проверки правописания на русском
def check_spelling_ru(word):
    dictionary = enchant.Dict('ru_Ru')
    check_result = dictionary.check(word)
    return check_result


# Фун-ия перевода
def google_translate_word(word):
    try:
        translator = Translator()

        word_translate = ''
        # Определяем язык переводимого слова
        check_lang = translator.translate(word).src
        if check_lang == 'ru':
            word_translate = translator.translate(word, dest='en').text
        if check_lang == 'en':
            word_translate = translator.translate(word, dest='ru').text

        return word_translate

    except AttributeError as error:
        print(error.args)
        print(word)


# Получение рандомного слова из списка английских слов
def get_random_word(user_id):
    rnd_words_list = database.get_eng_words()

    rnd_num = random.randint(0, len(rnd_words_list))
    rnd_word = rnd_words_list[rnd_num][0]

    # Проверка правописания полученного слова
    while not check_spelling_en(rnd_word):
        rnd_num = random.randint(0, len(rnd_words_list))
        rnd_word = rnd_words_list[rnd_num][0]

    # Проверка, что полученное слово уже есть в словаре пользователя
    while database.check_repeat_word(user_id, rnd_word) > 0:
        rnd_num = random.randint(0, len(rnd_words_list))
        rnd_word = rnd_words_list[rnd_num][0]

    return rnd_word


# Функция составления теста
def get_test(user_id, num_questions):
    # easy - слова, которые пользователь знает лучше
    # medium - слова, которые пользователь знает средне
    # hard - слова, которые пользователь знает плохо
    easy_words_list = []
    medium_words_list = []
    hard_words_list = []

    # определяем кол-во слов для каждой группы
    num_easy_words = rounding_num(num_questions * 60 / 100)
    num_medium_words = rounding_num(num_questions * 25 / 100)
    num_hard_words = rounding_num(num_questions * 15 / 100)

    words_db_list = database.get_user_dict(user_id)

    # распределяем все слова по группам
    for word in words_db_list:
        if word[3] == 0:
            result_word_test = 0
        else:
            result_word_test = word[4] // word[3] * 100

        if result_word_test < 50:
            easy_words_list.append(word)

        elif 50 <= result_word_test < 75:
            medium_words_list.append(word)

        else:
            hard_words_list.append(word)

    # получаем для каждой группы нужное кол-ов слов (рандомно)
    test_group_easy = get_word_test(easy_words_list, num_easy_words)
    test_group_medium = get_word_test(medium_words_list, num_medium_words)
    test_group_hard = get_word_test(hard_words_list, num_hard_words)

    test_list = test_group_easy + test_group_medium + test_group_hard
    new_list = []

    # в случае если для одной из групп не хватает слов
    if len(test_group_easy) < num_easy_words or \
            len(test_group_medium) < num_medium_words or \
            len(test_group_hard) < num_hard_words:

        # Определяем кол-во нехват. слов
        num_missing_words = num_easy_words - len(test_group_easy) + \
                            num_medium_words - len(test_group_medium) + \
                            num_hard_words - len(test_group_hard)

        # исключаем уже выбранные слова
        for easy_word in easy_words_list:
            counter = 0
            for test_element in test_list:
                if easy_word == test_element:
                    counter += 1
            if counter < 1:
                new_list.append(easy_word)

        # выбираем оставшиеся слова
        missing_words_list = get_word_test(new_list, num_missing_words)
        test_list += missing_words_list

    # перемешиваем слова
    random.shuffle(test_list)

    # обновляем счетчик кол-ва раз, заданных в тесте
    for test_element in test_list:
        test_word = list(test_element)
        test_word[3] += 1
        database.set_ask_word(user_id, test_word[2], test_word[3])

    return test_list


# Фун-ия получения рандомных слов определенного кол-ва из списка
def get_word_test(words_list, num_list):
    if len(words_list) >= num_list:
        test_words_list = random.sample(words_list, num_list)

    else:
        test_words_list = words_list

    return test_words_list


# Правильное округление числа
def rounding_num(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num
