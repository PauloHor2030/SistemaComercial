# dao/item_venda_dao.py
from typing import List, Optional
from models.item_venda import ItemVenda
from db import Conexao

class ItemVendaDao:
    @staticmethod
    def inserir(m_item: ItemVenda) -> int:
        sql = """
        INSERT INTO t_item_venda (fk_idvenda, fk_idproduto, quantidade, preco_unitario)
        VALUES (%s, %s, %s, %s)
        """
        with Conexao().abrir() as cx:
            cur = cx.get_cursor
            cur.execute(sql, (m_item.m_fk_idvenda, m_item.m_fk_idproduto,
                              m_item.m_quantidade, m_item.m_preco_unitario))
            new_id = cur.lastrowid
            cx.fechar(True)
            return new_id

    @staticmethod
    def listar_por_venda(m_idvenda: int) -> List[ItemVenda]:
        sql = "SELECT * FROM t_item_venda WHERE fk_idvenda = %s ORDER BY id_item_venda"
        with Conexao().abrir() as cx:
            cur = cx.get_cursor
            cur.execute(sql, (m_idvenda,))
            rows = cur.fetchall()
            cx.fechar(False)
            return [ItemVenda(r["id_item_venda"], r["fk_idvenda"], r["fk_idproduto"],
                              r["quantidade"], float(r["preco_unitario"])) for r in rows]

    @staticmethod
    def remover(m_id_item: int) -> bool:
        sql = "DELETE FROM t_item_venda WHERE id_item_venda = %s"
        with Conexao().abrir() as cx:
            cur = cx.get_cursor
            cur.execute(sql, (m_id_item,))
            ok = cur.rowcount > 0
            cx.fechar(True)
            return ok
