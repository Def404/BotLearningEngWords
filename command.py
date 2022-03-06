import database
import enchant
from translate import Translator


def get_dictionary(user_id):
    dictionary_list = database.select_dictionary_db(user_id)
    coun = 0
    dictionary_list_res = []
    for element in dictionary_list:
        coun += 1

        translator = Translator(to_lang='Russian')
        word_translate = translator.translate(element[2])
        result_tests = 0
        if element[3] != 0:
            result_tests = element[4] // element[3] * 100
        word_list = [coun, element[2], word_translate, result_tests]

        dictionary_list_res.append(word_list)

    return dictionary_list_res


