from typing import List, Optional
from models import Produto
from .base_dao import get_conn_cursor

class ProdutoDAO:
    @staticmethod
    def inserir(produto: Produto) -> int:
        sql = """
            INSERT INTO t_produto (nome, preco, estoque)
            VALUES (%s, %s, %s)
        """
        with get_conn_cursor() as (conn, cur):
            cur.execute(sql, (produto.nome, produto.preco, produto.estoque))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def listar() -> List[Produto]:
        sql = "SELECT id_produto, nome, preco, estoque FROM t_produto ORDER BY id_produto"
        with get_conn_cursor(True) as (_, cur):
            cur.execute(sql)
            rows = cur.fetchall()
            return [Produto(**row) for row in rows]

    @staticmethod
    def buscar_por_id(id_produto: int) -> Optional[Produto]:
        sql = "SELECT id_produto, nome, preco, estoque FROM t_produto WHERE id_produto = %s"
        with get_conn_cursor(True) as (_, cur):
            cur.execute(sql, (id_produto,))
            row = cur.fetchone()
            return Produto(**row) if row else None

    @staticmethod
    def atualizar(produto: Produto) -> bool:
        sql = """
            UPDATE t_produto SET nome = %s, preco = %s, estoque = %s
            WHERE id_produto = %s
        """
        with get_conn_cursor() as (conn, cur):
            cur.execute(sql, (produto.nome, produto.preco, produto.estoque, produto.id_produto))
            conn.commit()
            return cur.rowcount > 0

    @staticmethod
    def remover(id_produto: int) -> bool:
        sql = "DELETE FROM t_produto WHERE id_produto = %s"
        with get_conn_cursor() as (conn, cur):
            cur.execute(sql, (id_produto,))
            conn.commit()
            return cur.rowcount > 0

    @staticmethod
    def debitar_estoque(id_produto: int, quantidade: int) -> bool:
        # Garante que não fique negativo
        sql = """
            UPDATE t_produto
               SET estoque = estoque - %s
             WHERE id_produto = %s AND estoque >= %s
        """
        with get_conn_cursor() as (conn, cur):
            cur.execute(sql, (quantidade, id_produto, quantidade))
            conn.commit()
            return cur.rowcount > 0