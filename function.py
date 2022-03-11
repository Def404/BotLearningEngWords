import enchant

from googletrans import Translator
from random_word import RandomWords


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
    r = RandomWords()
    random_word = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb", minCorpusCount=1, maxCorpusCount=10, minDictionaryCount=1, maxDictionaryCount=10)
    print(str(check_spelling_en(random_word)) + ' ' + random_word)
    while not check_spelling_en(random_word):
        print(str(check_spelling_en(random_word)) + ' ' + random_word)
        random_word = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb", minCorpusCount=1, maxCorpusCount=10, minDictionaryCount=1, maxDictionaryCount=10)

    while database.check_repeat_word(user_id, random_word)[0][0] > 0:
        random_word = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb", minCorpusCount=1, maxCorpusCount=10, minDictionaryCount=1, maxDictionaryCount=10)

    return random_word
