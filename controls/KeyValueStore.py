import sqlite3
import threading
from contextlib import contextmanager
import os

class KeyValueStore:
    def __init__(self):
        user_path = os.path.expanduser('~')
        dir_path = os.path.join(user_path, ".lucidlinkFrameIOapp")
        self._create_app_dir(dir_path)
        db_file_path = f"{dir_path}/app.db"
        self._db_file = db_file_path
        self._local = threading.local()
        self._init_db()

    def _create_app_dir(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            os.chmod(dir_path, 0o700)
            print(f"Directory {dir_path} created successfully with permissions 700")
        else:
            pass

    def _init_db(self):
        with self._connect() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS key_value_store (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')

    @contextmanager
    def _connect(self):
        conn = getattr(self._local, 'connection', None)
        if conn is None:
            conn = sqlite3.connect(self._db_file)
            self._local.connection = conn
        try:
            yield conn
        finally:
            if getattr(self._local, 'connection', None) is not None:
                self._local.connection.close()
                del self._local.connection

    def set(self, key, value):
        with self._connect() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO key_value_store (key, value)
                VALUES (?, ?)
            ''', (key, value))
            conn.commit()  # Commit changes to the database

    def get(self, key):
        with self._connect() as conn:
            cursor = conn.execute('''
                SELECT value FROM key_value_store WHERE key=?
            ''', (key,))
            result = cursor.fetchone()
            return result[0] if result else None

    def delete(self, key):
        with self._connect() as conn:
            conn.execute('''
                DELETE FROM key_value_store WHERE key=?
            ''', (key,))
            conn.commit()  # Commit changes to the database

    def get_all(self):
        with self._connect() as conn:
            cursor = conn.execute('''
                SELECT key, value FROM key_value_store
            ''')
            return cursor.fetchall()

    def close(self):
        if hasattr(self._local, 'connection') and self._local.connection is not None:
            self._local.connection.close()
            del self._local.connection

# Example usage
if __name__ == "__main__":
    kv_store = KeyValueStore()
    kv_store.set("name", "John")
    kv_store.set("age", 30)
    print(kv_store.get_all())  # Output: [('name', 'John'), ('age', 30)]
    kv_store.close()