import sqlite3


# Получение всех слов пользователя из словаря
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


# Получение всех анг слов
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


# Добавление в словарь нового слова
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


# Проверка наличия слова в словаре
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


# Удаление слова из словаря
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


# Удаление всех слов из словаря
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


# Получение количество слов в словаре пользователя
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


# Обновление счетчика кол-ва попавш. раз в тесте для слова
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


# Получение слова из словаря по ID
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


# Обновление счетчика кол-ва раз правильных ответов в тесте для слова
def set_answer_word(user_id, word):
    new_answered = 0
    # Сначала получаем предыдущие значение
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
    # Обновляем
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
