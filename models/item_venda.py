# models/item_venda.py
from dataclasses import dataclass

@dataclass
class ItemVenda:
    m_id_item_venda: int
    m_fk_idvenda: int
    m_fk_idproduto: int
    m_quantidade: int
    m_preco_unitario: float
