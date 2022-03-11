import enchant
from translate import Translator
from googletrans import Translator


# function for checking spelling english words
def check_spelling_en(word):
    dictionary = enchant.Dict('en_US')
    check_result = dictionary.check(word)
    return check_result


def check_spelling_ru(word):
    dictionary = enchant.Dict('ru_Ru')
    result = dictionary.check(word)
    return result


def translate_word(word, from_lang, to_lang):
    translator = Translator(to_lang=to_lang)
    word_translate = translator.translate(word)
    return word_translate


def google_translate_word(word):

    translator = Translator()

    word_translate = ''
    check_lang = translator.translate(word).src
    if check_lang == 'ru':
        word_translate = translator.translate(word, dest='en')
    if check_lang == 'en':
        word_translate = translator.translate(word, dest='ru')

    return word_translate.text
