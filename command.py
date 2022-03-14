import database


def get_dictionary(user_id):

    dictionary_list = database.select_dictionary_db(user_id)
    count = 0
    dictionary_list_res = []

    for element in dictionary_list:

        count += 1

        result_tests = 0

        if element[3] != 0:
            result_tests = element[4] // element[3] * 100

        word_list = [count, element[2], element[5], result_tests]

        dictionary_list_res.append(word_list)

    return dictionary_list_res


