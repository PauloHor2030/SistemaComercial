import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
from typing import Iterator
from config import DB

class DatabasePool:
    _pool: pooling.MySQLConnectionPool | None = None

    @classmethod
    def get_pool(cls) -> pooling.MySQLConnectionPool:
        if cls._pool is None:
            cls._pool = pooling.MySQLConnectionPool(
                pool_name="pool_sistema",
                pool_size=5,
                host=DB.host,
                user=DB.user,
                password=DB.password,
                database=DB.database,
                charset="utf8mb4",
                collation="utf8mb4_unicode_ci",
            )
        return cls._pool

@contextmanager
def get_conn_cursor(dict_cursor: bool = False) -> Iterator[tuple]:
    conn = DatabasePool.get_pool().get_connection()
    try:
        cursor = conn.cursor(dictionary=dict_cursor)
        yield conn, cursor
        cursor.close()
        conn.close()
    except Exception:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
        raise