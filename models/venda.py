# models/venda.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Venda:
    id_venda: int
    data_hora: datetime | None
    numero_itens: int
    total: float
    fk_id_cliente: int