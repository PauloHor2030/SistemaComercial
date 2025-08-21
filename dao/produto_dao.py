from typing import List, Optional
from db import Conexao
from models.produto import Produto

class ProdutoDao:
    @staticmethod
    def inserir(produto: Produto) -> int:
        sql = "INSERT INTO t_produto (nome_produto, preco, estoque) VALUES (%s, %s, %s)"
        with Conexao().abrir() as cx:
            cx.cur.execute(sql, (produto.nome_produto, produto.preco, produto.estoque))
            return cx.cur.lastrowid

    @staticmethod
    def listar() -> List[Produto]:
        sql = "SELECT id_produto, nome_produto, preco, estoque FROM t_produto ORDER BY id_produto"
        with Conexao().abrir(dict_cursor=True) as cx:
            cx.cur.execute(sql)
            rows = cx.cur.fetchall()
            return [Produto(**row) for row in rows]

    @staticmethod
    def buscar_por_id(id_produto: int) -> Optional[Produto]:
        sql = "SELECT id_produto, nome_produto, preco, estoque FROM t_produto WHERE id_produto = %s"
        with Conexao().abrir(dict_cursor=True) as cx:
            cx.cur.execute(sql, (id_produto,))
            row = cx.cur.fetchone()
            return Produto(**row) if row else None

    @staticmethod
    def atualizar(produto: Produto) -> bool:
        sql = "UPDATE t_produto SET nome_produto=%s, preco=%s, estoque=%s WHERE id_produto=%s"
        with Conexao().abrir() as cx:
            cx.cur.execute(sql, (produto.nome_produto, produto.preco, produto.estoque, produto.id_produto))
            return cx.cur.rowcount > 0

    @staticmethod
    def remover(id_produto: int) -> bool:
        sql = "DELETE FROM t_produto WHERE id_produto=%s"
        with Conexao().abrir() as cx:
            cx.cur.execute(sql, (id_produto,))
            return cx.cur.rowcount > 0
