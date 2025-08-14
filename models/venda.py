# models/venda.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Venda:
    m_id_venda: int
    m_data_hora: datetime | None
    m_numero_itens: int
    m_total: float
    m_fk_id_cliente: int