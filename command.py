import database
import enchant


def add_word(user_id, word):
    # проверка на правописание
    dictionary = enchant.Dict('en_US')
    dictionary_check = dictionary.check(word)

    # проверка на повтор
    find_in = database.find_repid_word(user_id, word)[0][0]

    if not dictionary_check:
        return 'Слово содержит ошибки'
    elif find_in > 0:
        return 'Слово уже есть в словаре'
    else:
        database.insert_dictionary_db(user_id, word)
        return 'Слово добавлено'


def get_dictionary(user_id):
    dictionary_list = database.select_dictionary_db(user_id)
    coun = 0
    dictionary_list_res = []
    for element in dictionary_list:
        coun += 1

        word_list = []
        word_list.append(coun)
        word_list.append(element[2])

        dictionary_list_res.append(word_list)
        # print(element)

    print(dictionary_list_res)