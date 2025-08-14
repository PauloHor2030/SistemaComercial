from typing import List, Optional
from models import Cliente
from .base_dao import get_conn_cursor

class ClienteDAO:
    @staticmethod
    def inserir(cliente: Cliente) -> int:
        sql = """
            INSERT INTO t_cliente (nome, email, telefone)
            VALUES (%s, %s, %s)
        """
        with get_conn_cursor() as (conn, cur):
            cur.execute(sql, (cliente.nome, cliente.email, cliente.telefone))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def listar() -> List[Cliente]:
        sql = "SELECT id_cliente, nome, email, telefone FROM t_cliente ORDER BY id_cliente"
        with get_conn_cursor(True) as (_, cur):
            cur.execute(sql)
            rows = cur.fetchall()
            return [Cliente(**row) for row in rows]

    @staticmethod
    def buscar_por_id(id_cliente: int) -> Optional[Cliente]:
        sql = "SELECT id_cliente, nome, email, telefone FROM t_cliente WHERE id_cliente = %s"
        with get_conn_cursor(True) as (_, cur):
            cur.execute(sql, (id_cliente,))
            row = cur.fetchone()
            return Cliente(**row) if row else None

    @staticmethod
    def atualizar(cliente: Cliente) -> bool:
        sql = """
            UPDATE t_cliente SET nome = %s, email = %s, telefone = %s
            WHERE id_cliente = %s
        """
        with get_conn_cursor() as (conn, cur):
            cur.execute(sql, (cliente.nome, cliente.email, cliente.telefone, cliente.id_cliente))
            conn.commit()
            return cur.rowcount > 0

    @staticmethod
    def remover(id_cliente: int) -> bool:
        sql = "DELETE FROM t_cliente WHERE id_cliente = %s"
        with get_conn_cursor() as (conn, cur):
            cur.execute(sql, (id_cliente,))
            conn.commit()
            return cur.rowcount > 0
