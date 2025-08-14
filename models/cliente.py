# models/cliente.py
from dataclasses import dataclass
from datetime import date

@dataclass
class Cliente:
    m_id_cliente: int
    m_nome: str
    m_sobrenome: str
    m_data_nascimento: date | None
    m_email: str | None
    m_telefone: str | None
    m_cpf: str