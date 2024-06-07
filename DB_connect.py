import sqlite3


def create_database():
    db_connection = sqlite3.connect('db_name.db')
    cursor_db = db_connection.cursor()

    cursor_db.execute("DROP TABLE IF EXISTS homes")

    table = """ CREATE TABLE homes (
                id INTEGER PRIMARY KEY NOT NULL,
                suburb VARCHAR(255) NOT NULL,
                address VARCHAR(255) NOT NULL,
                price INTEGER NOT NULL
                ); """

    cursor_db.execute(table)

    db_connection.commit()
    db_connection.close()
