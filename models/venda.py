from dataclasses import dataclass
from datetime import datetime

@dataclass
class Venda:
    id_venda: int | None
    id_cliente: int
    data_venda: datetime | None = None
    total: float = 0.0