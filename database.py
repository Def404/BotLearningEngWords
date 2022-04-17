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


def get_user_dict(user_id):
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


def get_eng_words():
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


def set_user_word(user_id, word, word_translate):
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
        return cursor.fetchall()[0][0]

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


def count_user_words(user_id):
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


def set_ask_word(user_id, word, new_ask):
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


def get_word_by_id(word_id):
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM user_dictionary WHERE Id=:id", {"id": word_id})
        return cursor.fetchall()

    except sqlite3.Error as error:
        print(error.args)
        s = []
        return s

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def set_answer_word(user_id, word):
    new_answered = 0
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT Answered FROM user_dictionary WHERE Uid=(?) and Word=(?)", (user_id, word))
        new_answered = cursor.fetchall()[0][0]

    except sqlite3.Error as error:
        print(error.args)

    finally:
        if sqlite_connection:
            sqlite_connection.close()

    new_answered += 1

    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("UPDATE user_dictionary SET Answered=(?) WHERE Uid=(?) and Word=(?)",
                       (new_answered, user_id, word))
        sqlite_connection.commit()

    except sqlite3.Error as error:
        print(error.args)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
