from typing import List
from models import Cliente, Produto, Venda, ItemVenda
from dao.cliente_dao import ClienteDAO
from dao.produto_dao import ProdutoDAO
from dao.venda_dao import VendaDAO

# Helpers de input seguro

def input_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Valor inválido. Digite um número inteiro.")

def input_float(msg: str) -> float:
    while True:
        try:
            return float(input(msg).replace(",", "."))
        except ValueError:
            print("Valor inválido. Digite um número (use vírgula ou ponto).")

# Menus

def menu_principal():
    print("\n=== SISTEMA COMERCIAL ===")
    print("[1] Clientes")
    print("[2] Produtos")
    print("[3] Vendas")
    print("[0] Sair")
    return input_int("Escolha: ")


def menu_clientes():
    print("\n--- CLIENTES ---")
    print("[1] Cadastrar")
    print("[2] Listar")
    print("[3] Buscar por ID")
    print("[4] Atualizar")
    print("[5] Remover")
    print("[0] Voltar")
    return input_int("Escolha: ")


def menu_produtos():
    print("\n--- PRODUTOS ---")
    print("[1] Cadastrar")
    print("[2] Listar")
    print("[3] Buscar por ID")
    print("[4] Atualizar")
    print("[5] Remover")
    print("[0] Voltar")
    return input_int("Escolha: ")


def menu_vendas():
    print("\n--- VENDAS ---")
    print("[1] Registrar nova venda")
    print("[2] Listar vendas")
    print("[3] Detalhar venda por ID")
    print("[0] Voltar")
    return input_int("Escolha: ")


# Fluxos

def fluxo_clientes():
    while True:
        op = menu_clientes()
        if op == 0:
            break
        elif op == 1:
            nome = input("Nome: ")
            email = input("Email (opcional): ") or None
            telefone = input("Telefone (opcional): ") or None
            novo = Cliente(None, nome, email, telefone)
            idc = ClienteDAO.inserir(novo)
            print(f"Cliente cadastrado com ID {idc}")
        elif op == 2:
            for c in ClienteDAO.listar():
                print(c)
        elif op == 3:
            idc = input_int("ID do cliente: ")
            c = ClienteDAO.buscar_por_id(idc)
            print(c if c else "Não encontrado.")
        elif op == 4:
            idc = input_int("ID do cliente: ")
            c = ClienteDAO.buscar_por_id(idc)
            if not c:
                print("Não encontrado.")
                continue
            nome = input(f"Nome [{c.nome}]: ") or c.nome
            email = input(f"Email [{c.email or ''}]: ") or c.email
            telefone = input(f"Telefone [{c.telefone or ''}]: ") or c.telefone
            c.nome, c.email, c.telefone = nome, email, telefone
            ok = ClienteDAO.atualizar(c)
            print("Atualizado!" if ok else "Nada alterado.")
        elif op == 5:
            idc = input_int("ID do cliente: ")
            ok = ClienteDAO.remover(idc)
            print("Removido." if ok else "ID inexistente.")


def fluxo_produtos():
    while True:
        op = menu_produtos()
        if op == 0:
            break
        elif op == 1:
            nome = input("Nome: ")
            preco = input_float("Preço: ")
            estoque = input_int("Estoque inicial: ")
            novo = Produto(None, nome, preco, estoque)
            pid = ProdutoDAO.inserir(novo)
            print(f"Produto cadastrado com ID {pid}")
        elif op == 2:
            for p in ProdutoDAO.listar():
                print(p)
        elif op == 3:
            pid = input_int("ID do produto: ")
            p = ProdutoDAO.buscar_por_id(pid)
            print(p if p else "Não encontrado.")
        elif op == 4:
            pid = input_int("ID do produto: ")
            p = ProdutoDAO.buscar_por_id(pid)
            if not p:
                print("Não encontrado.")
                continue
            nome = input(f"Nome [{p.nome}]: ") or p.nome
            preco_in = input(f"Preço [{p.preco}]: ")
            estoque_in = input(f"Estoque [{p.estoque}]: ")
            preco = float(preco_in.replace(",", ".")) if preco_in else p.preco
            estoque = int(estoque_in) if estoque_in else p.estoque
            p.nome, p.preco, p.estoque = nome, preco, estoque
            ok = ProdutoDAO.atualizar(p)
            print("Atualizado!" if ok else "Nada alterado.")
        elif op == 5:
            pid = input_int("ID do produto: ")
            ok = ProdutoDAO.remover(pid)
            print("Removido." if ok else "ID inexistente.")


def fluxo_vendas():
    while True:
        op = menu_vendas()
        if op == 0:
            break
        elif op == 1:
            id_cliente = input_int("ID do cliente: ")
            itens: List[ItemVenda] = []
            while True:
                pid = input_int("ID do produto (0 para finalizar): ")
                if pid == 0:
                    break
                prod = ProdutoDAO.buscar_por_id(pid)
                if not prod:
                    print("Produto não encontrado.")
                    continue
                qtd = input_int("Quantidade: ")
                itens.append(ItemVenda(None, None, pid, qtd, prod.preco, prod.preco * qtd))
            if not itens:
                print("Nenhum item informado. Cancelado.")
                continue
            try:
                idv = VendaDAO.inserir_venda_com_itens(Venda(None, id_cliente), itens)
                print(f"Venda registrada com ID {idv}")
            except Exception as e:
                print(f"Falha ao registrar venda: {e}")
        elif op == 2:
            vendas = VendaDAO.listar_vendas()
            for v in vendas:
                print(f"Venda {v['id_venda']} | Cliente: {v['cliente']} | Data: {v['data_venda']} | Total: {v['total']}")
        elif op == 3:
            idv = input_int("ID da venda: ")
            det = VendaDAO.detalhar_venda(idv)
            if not det:
                print("Venda não encontrada.")
                continue
            print(f"Venda {det['id_venda']} | Cliente: {det['cliente']} | Data: {det['data_venda']} | Total: {det['total']}")
            for it in det["itens"]:
                print(f"  - {it['produto']} x{it['quantidade']} @ {it['preco_unitario']} = {it['subtotal']}")


if __name__ == "__main__":
    while True:
        op = menu_principal()
        if op == 0:
            print("Até logo!")
            break
        elif op == 1:
            fluxo_clientes()
        elif op == 2:
            fluxo_produtos()
        elif op == 3:
            fluxo_vendas()