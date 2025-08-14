from dataclasses import dataclass

@dataclass
class Produto:
    id_produto: int | None
    nome: str
    preco: float
    estoque: int