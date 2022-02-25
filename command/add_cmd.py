import database


def add_word(user_id, word):
    # проверка...
    print(user_id)
    print(word)
    database.insert_dictionary_db(user_id, word)
