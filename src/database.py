# src/database.py
import sqlite3
import os
from pathlib import Path


class Database:
    def __init__(self, db_path):
        # Создаем директорию для БД если её нет
        Path(os.path.dirname(db_path)).mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS monitoring_sites
                (user_id INTEGER, url TEXT,
                PRIMARY KEY (user_id, url))
            ''')

    def add_site(self, user_id: int, url: str):
        with self.conn:
            self.conn.execute(
                'INSERT OR REPLACE INTO monitoring_sites (user_id, url) VALUES (?, ?)',
                (user_id, url)
            )

    def remove_site(self, user_id: int):
        with self.conn:
            self.conn.execute(
                'DELETE FROM monitoring_sites WHERE user_id = ?',
                (user_id,)
            )

    def get_all_sites(self):
        cursor = self.conn.execute('SELECT user_id, url FROM monitoring_sites')
        return cursor.fetchall()
