import enchant
from translate import Translator


# function for checking spelling english words
def check_spelling(word):
    dictionary = enchant.Dict('en_US')
    check_result = dictionary.check(word)
    return check_result


def translate_word(word, from_lang, to_lang):
    translator = Translator(to_lang=to_lang)
    word_translate = translator.translate(word)
    return word_translate
