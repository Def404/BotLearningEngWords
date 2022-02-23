import sqlite3


def created_db():
    try:
        sqlite_connection = sqlite3.connect('tg_database.db')
        cursor = sqlite_connection.cursor()
        print('Connection successful')

    except sqlite3.Error as error:
        print(error.args)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Connection close")