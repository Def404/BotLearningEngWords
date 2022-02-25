import database


def get_dictionary(user_id):
    dictionary_list = database.select_dictionary_db(user_id)

