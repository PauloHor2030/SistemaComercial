-- Banco e tabelas com prefixo t_
CREATE DATABASE IF NOT EXISTS sistema_comercial CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sistema_comercial;

-- CLIENTE
CREATE TABLE IF NOT EXISTS t_cliente (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(120) UNIQUE,
  telefone VARCHAR(20),
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- PRODUTO
CREATE TABLE IF NOT EXISTS t_produto (
  id_produto INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  preco DECIMAL(10,2) NOT NULL CHECK (preco >= 0),
  estoque INT NOT NULL DEFAULT 0 CHECK (estoque >= 0),
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- VENDA (cabeçalho)
CREATE TABLE IF NOT EXISTS t_venda (
  id_venda INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente INT NOT NULL,
  data_venda DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total DECIMAL(12,2) NOT NULL DEFAULT 0,
  CONSTRAINT fk_venda_cliente FOREIGN KEY (id_cliente)
    REFERENCES t_cliente(id_cliente) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ITEM_VENDA (itens)
CREATE TABLE IF NOT EXISTS t_item_venda (
  id_item INT AUTO_INCREMENT PRIMARY KEY,
  id_venda INT NOT NULL,
  id_produto INT NOT NULL,
  quantidade INT NOT NULL CHECK (quantidade > 0),
  preco_unitario DECIMAL(10,2) NOT NULL CHECK (preco_unitario >= 0),
  subtotal DECIMAL(12,2) NOT NULL,
  CONSTRAINT fk_item_venda_venda FOREIGN KEY (id_venda)
    REFERENCES t_venda(id_venda) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_item_venda_produto FOREIGN KEY (id_produto)
    REFERENCES t_produto(id_produto) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Índices úteis
CREATE INDEX IF NOT EXISTS idx_venda_cliente ON t_venda(id_cliente, data_venda);
CREATE INDEX IF NOT EXISTS idx_item_produto ON t_item_venda(id_produto);