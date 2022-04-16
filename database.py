import sqlite3


def created_db():
    try:
        sqlite_connection = sqlite3.connect('tg_database.db', isolation_level=None)
        cursor = sqlite_connection.cursor()
        print('Connection successful')

    except sqlite3.Error as error:
        print(error.args)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Connection close")


def select_dictionary_db(user_id):
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM user_dictionary WHERE Uid=:user_id", {"user_id": user_id})
        return cursor.fetchall()

    except sqlite3.Error as error:
        print(error.args)
        s = []
        return s

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def select_eng_words():
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM eng_words_dictionary")
        return cursor.fetchall()

    except sqlite3.Error as error:
        print(error.args)
        s = []
        return s

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def insert_dictionary_db(user_id, word, word_translate):

    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()

        cursor.execute("INSERT INTO user_dictionary (Uid, Word, TranslateWord,Asked, Answered) VALUES (?,?,?,0,0)",
                       (user_id, word, word_translate))

        sqlite_connection.commit()

    except sqlite3.Error as error:
        print(error.args)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def check_repeat_word(user_id, word):
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT COUNT() FROM user_dictionary WHERE Uid=(?) AND Word=(?)", (user_id, word))
        return cursor.fetchall()

    except sqlite3.Error as error:
        print(error.args)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def delete_word(user_id, word):
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()

        cursor.execute("DELETE FROM user_dictionary WHERE Uid=(?) AND Word=(?)", (user_id, word))
        sqlite_connection.commit()

    except sqlite3.Error as error:
        print(error.args)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_words():
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT word FROM eng_words_dictionary")
        return cursor.fetchall()

    except sqlite3.Error as error:
        print(error.args)
        s = []
        return s

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def del_dict_user(user_id):
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()

        cursor.execute("DELETE FROM user_dictionary WHERE Uid=(?)", (user_id,))
        sqlite_connection.commit()

    except sqlite3.Error as error:
        print(error.args)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def count_user_dict(user_id):
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT COUNT() FROM user_dictionary WHERE Uid=(?)", (user_id,))
        return cursor.fetchall()[0][0]

    except sqlite3.Error as error:
        print(error.args)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def update_ask(user_id, word, new_ask):
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("UPDATE user_dictionary SET Asked=(?) WHERE Uid=(?) and Word=(?)", (new_ask, user_id, word))
        sqlite_connection.commit()

    except sqlite3.Error as error:
        print(error.args)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_word_by_id(id):
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM user_dictionary WHERE Id=:id", {"id": id})
        return cursor.fetchall()

    except sqlite3.Error as error:
        print(error.args)
        s = []
        return s

    finally:
        if sqlite_connection:
            sqlite_connection.close()
