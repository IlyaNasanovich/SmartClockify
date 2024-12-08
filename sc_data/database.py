from config import DB_PATH
from sqlite3 import connect


def execute_query(query: str, args=()):
    with connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()


def get_all(query: str, args=()):
    with connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        return cursor.fetchall()


def get_one(query: str, args=()):
    with connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        return cursor.fetchone()
