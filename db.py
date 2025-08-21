# db.py
import mysql.connector

class Conexao:
    def __init__(self, *, host='localhost', user='root', password='senai110', database='db_comercial'):
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._conn = None
        self._cursor = None
        self._dict_cursor = False

    def abrir(self, dict_cursor: bool = False):
        """Permite: with Conexao().abrir(dict_cursor=True) as cx:"""
        self._dict_cursor = dict_cursor
        self._conn = mysql.connector.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            database=self._database
        )
        self._cursor = self._conn.cursor(dictionary=dict_cursor)
        return self

    # --- Context manager ---
    def __enter__(self):
        if self._conn is None or self._cursor is None:
            self.abrir(self._dict_cursor)#77
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type is not None:
                self._conn.rollback()
            else:
                self._conn.commit()
        finally:
            try:
                if self._cursor:
                    self._cursor.close()
            finally:
                if self._conn:
                    self._conn.close()

    # --- Propriedades modernas esperadas pelos novos DAOs ---
    @property
    def conn(self):
        return self._conn

    @property
    def cur(self):
        return self._cursor

    # --- Aliases de compatibilidade (código antigo) ---
    @property
    def get_conexao(self):
        return self._conn

    @property
    def get_cursor(self):
        return self._cursor
