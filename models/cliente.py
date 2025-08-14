from dataclasses import dataclass

@dataclass
class Cliente:
    id_cliente: int | None
    nome: str
    email: str | None = None
    telefone: str | None = None