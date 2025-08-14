from dataclasses import dataclass

@dataclass
class ItemVenda:
    id_item: int | None
    id_venda: int | None
    id_produto: int
    quantidade: int
    preco_unitario: float
    subtotal: float