from typing import List, Sequence
from models import Venda, ItemVenda
from .base_dao import get_conn_cursor
from .produto_dao import ProdutoDAO

class VendaDAO:
    @staticmethod
    def inserir_venda_com_itens(venda: Venda, itens: Sequence[ItemVenda]) -> int:
        """Insere venda + itens em transação; debita estoque e calcula total.
        Lança exceção para rollback automático do with, se falhar.
        """
        with get_conn_cursor() as (conn, cur):
            try:
                # 1) Cabeçalho da venda
                cur.execute(
                    "INSERT INTO t_venda (id_cliente, total) VALUES (%s, %s)",
                    (venda.id_cliente, 0.0),
                )
                id_venda = cur.lastrowid

                total = 0.0
                # 2) Itens + estoque
                for it in itens:
                    # Verifica e debita estoque no ato
                    if not ProdutoDAO.debitar_estoque(it.id_produto, it.quantidade):
                        raise ValueError(f"Estoque insuficiente para o produto {it.id_produto}")

                    subtotal = round(it.preco_unitario * it.quantidade, 2)
                    total += subtotal

                    cur.execute(
                        """
                        INSERT INTO t_item_venda (id_venda, id_produto, quantidade, preco_unitario, subtotal)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (id_venda, it.id_produto, it.quantidade, it.preco_unitario, subtotal),
                    )

                # 3) Atualiza total no cabeçalho
                cur.execute("UPDATE t_venda SET total = %s WHERE id_venda = %s", (total, id_venda))
                conn.commit()
                return id_venda
            except Exception as e:
                conn.rollback()
                raise e

    @staticmethod
    def listar_vendas() -> list[dict]:
        sql = """
            SELECT v.id_venda, v.data_venda, v.total, c.id_cliente, c.nome AS cliente
              FROM t_venda v
              JOIN t_cliente c ON c.id_cliente = v.id_cliente
             ORDER BY v.id_venda DESC
        """
        with get_conn_cursor(True) as (_, cur):
            cur.execute(sql)
            vendas = cur.fetchall()
            return vendas

    @staticmethod
    def detalhar_venda(id_venda: int) -> dict | None:
        cab_sql = """
            SELECT v.id_venda, v.data_venda, v.total, c.id_cliente, c.nome AS cliente
              FROM t_venda v
              JOIN t_cliente c ON c.id_cliente = v.id_cliente
             WHERE v.id_venda = %s
        """
        itens_sql = """
            SELECT iv.id_item, p.nome AS produto, iv.quantidade, iv.preco_unitario, iv.subtotal
              FROM t_item_venda iv
              JOIN t_produto p ON p.id_produto = iv.id_produto
             WHERE iv.id_venda = %s
             ORDER BY iv.id_item
        """
        with get_conn_cursor(True) as (_, cur):
            cur.execute(cab_sql, (id_venda,))
            cab = cur.fetchone()
            if not cab:
                return None
            cur.execute(itens_sql, (id_venda,))
            itens = cur.fetchall()
            cab["itens"] = itens
            return cab