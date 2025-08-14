# app.py
from datetime import datetime
from models.cliente import Cliente
from models.produto import Produto
from models.venda import Venda
from models.item_venda import ItemVenda

from dao.cliente_dao import ClienteDao
from dao.produto_dao import ProdutoDao
from dao.venda_dao import VendaDao
from dao.item_venda_dao import ItemVendaDao

def m_input_int(msg):
    try:
        return int(input(msg))
    except Exception:
        print("Valor inválido.")
        return None

def menu_clientes():
    while True:
        print("\n[CLIENTES] 1-Listar 2-Detalhe 3-Cadastrar 4-Atualizar 5-Remover 0-Voltar")
        op = m_input_int("Opção: ")
        if op is None: 
            continue
        if op == 0: break
        if op == 1:
            for c in ClienteDao.listar():
                print(c)
        elif op == 2:
            m_id = m_input_int("ID: ")
            print(ClienteDao.buscar_por_id(m_id))
        elif op == 3:
            m_nome = input("Nome: ")
            m_sobrenome = input("Sobrenome: ")
            m_data = input("Data nasc (dd/mm/aaaa) ou vazio: ").strip()
            m_dn = datetime.strptime(m_data, "%d/%m/%Y").date() if m_data else None
            m_email = input("Email (opcional): ").strip() or None
            m_tel = input("Telefone (opcional): ").strip() or None
            m_cpf = input("CPF (000.000.000-00): ").strip()
            novo = Cliente(0, m_nome, m_sobrenome, m_dn, m_email, m_tel, m_cpf)
            print("Novo ID:", ClienteDao.inserir(novo))
        elif op == 4:
            m_id = m_input_int("ID para atualizar: ")
            cli = ClienteDao.buscar_por_id(m_id)
            if not cli:
                print("Cliente não encontrado.")
                continue
            cli.m_nome = input(f"Nome [{cli.m_nome}]: ") or cli.m_nome
            cli.m_sobrenome = input(f"Sobrenome [{cli.m_sobrenome}]: ") or cli.m_sobrenome
            m_data = input("Data nasc dd/mm/aaaa (enter p/ manter): ").strip()
            if m_data:
                cli.m_data_nascimento = datetime.strptime(m_data, "%d/%m/%Y").date()
            m_email = input(f"Email [{cli.m_email or ''}]: ").strip()
            cli.m_email = m_email or cli.m_email
            m_tel = input(f"Telefone [{cli.m_telefone or ''}]: ").strip()
            cli.m_telefone = m_tel or cli.m_telefone
            m_cpf = input(f"CPF [{cli.m_cpf}]: ").strip()
            cli.m_cpf = m_cpf or cli.m_cpf
            print("Atualizado?" , ClienteDao.atualizar(cli))
        elif op == 5:
            m_id = m_input_int("ID para remover: ")
            print("Removido?" , ClienteDao.remover(m_id))

def menu_produtos():
    while True:
        print("\n[PRODUTOS] 1-Listar 2-Detalhe 3-Cadastrar 4-Atualizar 5-Remover 0-Voltar")
        op = m_input_int("Opção: ")
        if op is None: 
            continue
        if op == 0: break
        if op == 1:
            for p in ProdutoDao.listar():
                print(p)
        elif op == 2:
            m_id = m_input_int("ID: ")
            print(ProdutoDao.buscar_por_id(m_id))
        elif op == 3:
            nome = input("Nome produto: ")
            preco = float(input("Preço: ").replace(",", "."))
            est = m_input_int("Estoque: ") or 0
            novo = Produto(0, nome, preco, est)
            print("Novo ID:", ProdutoDao.inserir(novo))
        elif op == 4:
            m_id = m_input_int("ID para atualizar: ")
            pro = ProdutoDao.buscar_por_id(m_id)
            if not pro:
                print("Produto não encontrado.")
                continue
            pro.m_nome_produto = input(f"Nome [{pro.m_nome_produto}]: ") or pro.m_nome_produto
            m_preco = input(f"Preço [{pro.m_preco}]: ").replace(",", ".").strip()
            pro.m_preco = float(m_preco) if m_preco else pro.m_preco
            m_est = input(f"Estoque [{pro.m_estoque}]: ").strip()
            pro.m_estoque = int(m_est) if m_est else pro.m_estoque
            print("Atualizado?", ProdutoDao.atualizar(pro))
        elif op == 5:
            m_id = m_input_int("ID para remover: ")
            print("Removido?", ProdutoDao.remover(m_id))

def menu_vendas():
    while True:
        print("\n[VENDAS] 1-Listar 2-Detalhe 3-Nova Venda 4-Adicionar Item 5-Remover Item 6-Excluir Venda 0-Voltar")
        op = m_input_int("Opção: ")
        if op is None: 
            continue
        if op == 0: break
        if op == 1:
            for v in VendaDao.listar():
                print(v)
        elif op == 2:
            m_id = m_input_int("ID da venda: ")
            v = VendaDao.buscar_por_id(m_id)
            if not v:
                print("Venda não encontrada.")
                continue
            print(v)
            for it in ItemVendaDao.listar_por_venda(m_id):
                print("   ", it)
        elif op == 3:
            id_cli = m_input_int("ID do cliente: ")
            ven = Venda(0, datetime.now(), 0, 0.0, id_cli)
            novo_id = VendaDao.inserir(ven)
            print("Venda criada ID:", novo_id)
        elif op == 4:
            id_v = m_input_int("ID da venda: ")
            id_p = m_input_int("ID do produto: ")
            qtd = m_input_int("Quantidade: ")
            pro = ProdutoDao.buscar_por_id(id_p)
            if not pro:
                print("Produto inexistente.")
                continue
            if qtd is None or qtd <= 0:
                print("Quantidade inválida.")
                continue
            it = ItemVenda(0, id_v, id_p, qtd, pro.m_preco)
            novo_item_id = ItemVendaDao.inserir(it)
            print("Item incluído ID:", novo_item_id, " — (totais da venda recalculados via trigger)")
        elif op == 5:
            id_item = m_input_int("ID do item para remover: ")
            print("Removido?", ItemVendaDao.remover(id_item))
        elif op == 6:
            id_v = m_input_int("ID da venda para excluir: ")
            print("Excluída?", VendaDao.remover(id_v))

def main():
    while True:
        print("\n=== SISTEMA COMERCIAL ===")
        print("1-Clientes  2-Produtos  3-Vendas  0-Sair")
        op = m_input_int("Opção: ")
        if op is None:
            continue
        if op == 0:
            print("Até logo!")
            break
        if op == 1:
            menu_clientes()
        elif op == 2:
            menu_produtos()
        elif op == 3:
            menu_vendas()

if __name__ == "__main__":
    main()
