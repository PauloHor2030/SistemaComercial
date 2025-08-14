# models/produto.py
from dataclasses import dataclass

@dataclass
class Produto:
    m_id_produto: int
    m_nome_produto: str
    m_preco: float
    m_estoque: int
