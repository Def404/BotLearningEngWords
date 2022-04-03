import enchant

from googletrans import Translator
import random

# function for checking spelling english words
import database


def check_spelling_en(word):
    dictionary = enchant.Dict('en_US')
    check_result = dictionary.check(word)
    return check_result


def check_spelling_ru(word):
    dictionary = enchant.Dict('ru_Ru')
    result = dictionary.check(word)
    return result


def google_translate_word(word):
    try:
        translator = Translator()

        word_translate = ''
        check_lang = translator.translate(word).src
        if check_lang == 'ru':
            word_translate = translator.translate(word, dest='en').text
        if check_lang == 'en':
            word_translate = translator.translate(word, dest='ru').text

        return word_translate

    except AttributeError as error:
        print(error.args)
        print(word)


def get_random_word(user_id):
    words = database.get_words()

    rnd = random.randint(0, len(words))
    rnd_word = words[rnd][0]

    while not check_spelling_en(rnd_word):
        rnd = random.randint(0, len(words))
        rnd_word = words[rnd][0]

    while database.check_repeat_word(user_id, rnd_word)[0][0] > 0:
        rnd = random.randint(0, len(words))
        rnd_word = words[rnd][0]

    return rnd_word


def get_test(user_id, num_questions):
    test_list = []

    easy_words_list = []
    medium_words_list = []
    hard_words_list = []

    # определяем кол-во слов для каждой группы
    num_easy_words = int_r(num_questions * 60 / 100)
    num_medium_words = int_r(num_questions * 25 / 100)
    num_hard_words = int_r(num_questions * 15 / 100)

    words_db_list = database.select_dictionary_db(user_id)

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

    # print(test_group_easy)
    # print(test_group_medium)
    # print(test_group_hard)

    # в случает если для одной из групп не хватает слов
    if len(test_group_easy) < num_easy_words or \
            len(test_group_medium) < num_medium_words or \
            len(test_group_hard) < num_hard_words:

        # определяем кол-во нехват. слов
        cont = num_easy_words - len(test_group_easy) + \
               num_medium_words - len(test_group_medium) + \
               num_hard_words - len(test_group_hard)

        # исключаем уже выбранные слова
        for el in easy_words_list:
            counter = 0
            for el_2 in test_list:
                if el == el_2:
                    counter += 1
            if counter < 1:
                new_list.append(el)

        # print(new_list)
        # выбираем оставшиеся слова
        missing_words_list = get_word_test(new_list, cont)
        # print(missing_words_list)
        test_list += missing_words_list

    # перемешиваем слова
    random.shuffle(test_list)

    # обновляем счетчик кол-ва раз, заданных в тесте
    for test_el in test_list:
        test_el_list = list(test_el)
        test_el_list[3] += 1
        database.update_ask(user_id, test_el_list[2], test_el_list[3])

    return test_list


def get_word_test(words_list, num_list):
    if len(words_list) >= num_list:
        test_words_list = random.sample(words_list, num_list)

    else:
        test_words_list = words_list

    return test_words_list


def int_r(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num
