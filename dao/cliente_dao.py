from typing import List, Optional
from datetime import date
from db import Conexao
from models.cliente import Cliente


def _row_to_cliente(row: dict) -> Cliente:
    # Converte um dict do cursor (dict_cursor=True) para o seu dataclass Cliente (com prefixo m_)
    return Cliente(
        m_id_cliente=row["id_cliente"],
        m_nome=row["nome"],
        m_sobrenome=row.get("sobrenome"),
        m_data_nascimento=row.get("data_nascimento"),
        m_email=row.get("email"),
        m_telefone=row.get("telefone"),
        m_cpf=row.get("cpf"),
    )


class ClienteDao:
    @staticmethod
    def inserir(cliente: Cliente) -> int:
        """
        Insere um cliente (nome, sobrenome, data_nascimento, email, telefone, cpf).
        Retorna o ID gerado.
        """
        sql = """
            INSERT INTO t_cliente
                (nome, sobrenome, data_nascimento, email, telefone, cpf)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        with Conexao().abrir() as cx:
            cx.cur.execute(
                sql,
                (
                    cliente.m_nome,
                    cliente.m_sobrenome,
                    cliente.m_data_nascimento,  # pode ser None
                    cliente.m_email,
                    cliente.m_telefone,
                    cliente.m_cpf,
                ),
            )
            return cx.cur.lastrowid

    @staticmethod
    def listar() -> List[Cliente]:
        """
        Lista todos os clientes ordenados por id_cliente.
        """
        sql = """
            SELECT id_cliente, nome, sobrenome, data_nascimento, email, telefone, cpf
            FROM t_cliente
            ORDER BY id_cliente
        """
        with Conexao().abrir(dict_cursor=True) as cx:
            cx.cur.execute(sql)
            rows = cx.cur.fetchall()
            return [_row_to_cliente(r) for r in rows]

    @staticmethod
    def buscar_por_id(id_cliente: int) -> Optional[Cliente]:
        """
        Busca cliente pelo ID.
        """
        sql = """
            SELECT id_cliente, nome, sobrenome, data_nascimento, email, telefone, cpf
            FROM t_cliente
            WHERE id_cliente = %s
        """
        with Conexao().abrir(dict_cursor=True) as cx:
            cx.cur.execute(sql, (id_cliente,))
            row = cx.cur.fetchone()
            return _row_to_cliente(row) if row else None

    @staticmethod
    def buscar_por_cpf(cpf: str) -> Optional[Cliente]:
        """
        Busca cliente pelo CPF.
        """
        sql = """
            SELECT id_cliente, nome, sobrenome, data_nascimento, email, telefone, cpf
            FROM t_cliente
            WHERE cpf = %s
        """
        with Conexao().abrir(dict_cursor=True) as cx:
            cx.cur.execute(sql, (cpf,))
            row = cx.cur.fetchone()
            return _row_to_cliente(row) if row else None

    @staticmethod
    def buscar_por_nome_parcial(nome_parcial: str) -> List[Cliente]:
        """
        Busca por nome (LIKE).
        """
        like = f"%{nome_parcial}%"
        sql = """
            SELECT id_cliente, nome, sobrenome, data_nascimento, email, telefone, cpf
            FROM t_cliente
            WHERE nome LIKE %s
            ORDER BY nome, sobrenome
        """
        with Conexao().abrir(dict_cursor=True) as cx:
            cx.cur.execute(sql, (like,))
            rows = cx.cur.fetchall()
            return [_row_to_cliente(r) for r in rows]

    @staticmethod
    def atualizar(cliente: Cliente) -> bool:
        """
        Atualiza todos os campos do cliente (exceto id).
        Retorna True se alguma linha foi alterada.
        """
        if not cliente.m_id_cliente:
            raise ValueError("m_id_cliente é obrigatório para atualizar")

        sql = """
            UPDATE t_cliente
               SET nome = %s,
                   sobrenome = %s,
                   data_nascimento = %s,
                   email = %s,
                   telefone = %s,
                   cpf = %s
             WHERE id_cliente = %s
        """
        with Conexao().abrir() as cx:
            cx.cur.execute(
                sql,
                (
                    cliente.m_nome,
                    cliente.m_sobrenome,
                    cliente.m_data_nascimento,
                    cliente.m_email,
                    cliente.m_telefone,
                    cliente.m_cpf,
                    cliente.m_id_cliente,
                ),
            )
            return cx.cur.rowcount > 0

    @staticmethod
    def remover(id_cliente: int) -> bool:
        """
        Remove um cliente pelo ID.
        """
        sql = "DELETE FROM t_cliente WHERE id_cliente = %s"
        with Conexao().abrir() as cx:
            cx.cur.execute(sql, (id_cliente,))
            return cx.cur.rowcount > 0
