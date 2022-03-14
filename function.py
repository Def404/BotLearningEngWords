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
