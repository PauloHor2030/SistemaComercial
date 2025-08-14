# dao/venda_dao.py
from typing import List, Optional, Sequence
from db import Conexao
from models.venda import Venda
from models.item_venda import ItemVenda

class VendaDao:
    # 1) Listar
    @staticmethod
    def listar() -> List[dict]:
        sql = """
            SELECT v.id_venda, v.data_venda, v.total, c.id_cliente, c.nome AS cliente
            FROM t_venda v
            JOIN t_cliente c ON c.id_cliente = v.id_cliente
            ORDER BY v.id_venda DESC
        """
        with Conexao().abrir(dict_cursor=True) as cx:
            cx.cur.execute(sql)
            return cx.cur.fetchall()

    # 2) Detalhe
    @staticmethod
    def detalhe(id_venda: int) -> Optional[dict]:
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
        with Conexao().abrir(dict_cursor=True) as cx:
            cx.cur.execute(cab_sql, (id_venda,))
            cab = cx.cur.fetchone()
            if not cab:
                return None
            cx.cur.execute(itens_sql, (id_venda,))
            cab["itens"] = cx.cur.fetchall()
            return cab

    # 3) Nova Venda (cabeçalho + itens)
    @staticmethod
    def nova_venda(venda: Venda, itens: Sequence[ItemVenda]) -> int:
        """Insere venda + itens; triggers do banco atualizam total/estoque."""
        with Conexao().abrir() as cx:
            cx.cur.execute(
                "INSERT INTO t_venda (id_cliente, total) VALUES (%s, %s)",
                (venda.id_cliente, 0.0),
            )
            id_venda = cx.cur.lastrowid
            for it in itens:
                cx.cur.execute(
                    "INSERT INTO t_item_venda (id_venda, id_produto, quantidade, preco_unitario, subtotal) "
                    "VALUES (%s, %s, %s, %s, 0)",
                    (id_venda, it.id_produto, it.quantidade, it.preco_unitario),
                )
            return id_venda

    # 4) Adicionar Item
    @staticmethod
    def adicionar_item(id_venda: int, item: ItemVenda) -> int:
        """Adiciona 1 item em uma venda existente (triggers recalculam total/estoque)."""
        with Conexao().abrir() as cx:
            cx.cur.execute(
                "INSERT INTO t_item_venda (id_venda, id_produto, quantidade, preco_unitario, subtotal) "
                "VALUES (%s, %s, %s, %s, 0)",
                (id_venda, item.id_produto, item.quantidade, item.preco_unitario),
            )
            return cx.cur.lastrowid

    # 5) Remover Item
    @staticmethod
    def remover_item(id_item: int) -> bool:
        """Remove um item específico da venda (triggers estornam estoque/recalculam total)."""
        with Conexao().abrir() as cx:
            cx.cur.execute("DELETE FROM t_item_venda WHERE id_item = %s", (id_item,))
            return cx.cur.rowcount > 0

    # 6) Excluir Venda
    @staticmethod
    def excluir_venda(id_venda: int) -> bool:
        """Exclui a venda; itens caem via ON DELETE CASCADE e triggers estornam estoque."""
        with Conexao().abrir() as cx:
            cx.cur.execute("DELETE FROM t_venda WHERE id_venda = %s", (id_venda,))
            return cx.cur.rowcount > 0

    # Alias úteis (se seu app usar nomes diferentes em alguns pontos):
    @staticmethod
    def inserir_venda_com_itens(venda: Venda, itens: Sequence[ItemVenda]) -> int:
        return VendaDao.nova_venda(venda, itens)

    @staticmethod
    def detalhar_venda(id_venda: int) -> Optional[dict]:
        return VendaDao.detalhe(id_venda)
