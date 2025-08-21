# models/produto.py
from dataclasses import dataclass

@dataclass
class Produto:
    id_produto: int
    nome_produto: str
    preco: float
    estoque: int
