import sqlite3 as sq
import os
from config_data.config import HISTORY_NUM


def db_opener(func):
    def wraped_func(*args, **kwargs):
        con = None
        try:
            file_name = 'database' + os.path.sep + 'hotel_base.db'
            con = sq.connect(file_name)
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS history(
                    id INTEGER,
                    country TEXT,
                    city TEXT,
                    hotel_num INTEGER,
                    foto TEXT)
                    ''')
            value = func(cur, *args, **kwargs)
            con.commit()
            return value
        except sq.Error as e:
            if con:
                con.rollback()
                print('Ошибка записи! Данные не записаны!')
        finally:
            if con:
                con.close()
    return wraped_func


@db_opener
def db_loader(cur, user_id: int, country: str, city: str, hotel_num: int, foto: str):
    cur.execute('INSERT INTO history VALUES (?, ?, ?, ?, ?)', (user_id, country, city, hotel_num, foto))

@db_opener
def user_history(cur, user_id):
    cur.execute('SELECT country, city FROM history WHERE id LIKE ? ORDER BY _rowid_ DESC', (user_id,))
    select_history = cur.fetchmany(HISTORY_NUM)
    return select_history
