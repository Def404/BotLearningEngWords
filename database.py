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
        cursor.execute("SELECT * FROM dictionary WHERE Uid=:user_id", {"user_id": user_id})
        return cursor.fetchall()

    except sqlite3.Error as error:
        print(error.args)
        s = []
        return s

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def insert_dictionary_db(user_id, word):
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()

        cursor.execute("INSERT INTO dictionary (Uid, Word, Asked, Answered) VALUES (?,?,0,0)",  (user_id, word))
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
        cursor.execute("SELECT COUNT() FROM dictionary WHERE Uid=(?) AND Word=(?)", (user_id, word))
        return cursor.fetchall()

    except sqlite3.Error as error:
        print(error.args)

    finally:
        if sqlite_connection:
            sqlite_connection.close()