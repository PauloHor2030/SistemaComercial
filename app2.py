import  mysql.connector
from PyQt5 import uic, QtWidgets
try:
    conn = mysql.connector.connect(
        host= 'localhost',
        user= 'root',
        password= 'senai110',
        database= 'db_comercial'
    )
    cursor = conn.cursor()
    if conn.is_connected():
        print('Deu tudo certo com o MySQL')
except Exception as e:
    print('Deu ruim:', e)


sql = 'SELECT *  FROM t_produto;'

cursor.execute(sql)
dados = cursor.fetchall()

print(dados)

def buscar_por_id():
    id_campo = tela_produto.txt_id.text()
    sql = f'SELECT * FROM t_produto WHERE id_produto = {id_campo};'
    cursor.execute(sql)
    produto = cursor.fetchone()
    # preencher_campos(produto)
    print(produto)
    n_id = str(produto[0])
    n_descricao = str(produto[1])
    n_preco = str(produto[2])
    n_qtde = str(produto[3])

    tela_produto.txt_id.setText(n_id)
    tela_produto.txt_descricao.setText(n_descricao)
    tela_produto.txt_preco.setText(n_preco)
    tela_produto.txt_quantidade.setText(n_qtde)


# def abrir_tela_cadastro():
#     tela_produto2.show()

def botao_add():
    id = tela_produto.txt_id.text()
    descricao = tela_produto.txt_descricao.text()
    preco = tela_produto.txt_preco.text()
    quantidade = tela_produto.txt_quantidade.text()

    print(id, descricao, preco, quantidade)

def preencher_campos(produto):
    tela_produto.txt_id.setText(produto[0])
    tela_produto.txt_descricao.setText(produto[1])
    tela_produto.txt_preco.setText(produto[2])
    tela_produto.txt_quantidade.setText(produto[3])

app = QtWidgets.QApplication([])

tela_produto = uic.loadUi('tela_cadastro_produto.ui')
# tela_produto2 = uic.loadUi('tela_cadastro_produto2.ui')

tela_produto.show()
# tela_produto.btn_cadastrar.clicked.connect(abrir_tela_cadastro)
tela_produto.btn_add.clicked.connect(botao_add)
tela_produto.btn_editar.clicked.connect(buscar_por_id)
# tela_produto.btn_preencher.clicked.connect(buscar_por_id)
app.exec_()