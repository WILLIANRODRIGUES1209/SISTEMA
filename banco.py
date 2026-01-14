import sqlite3

# Conecta ao banco (se não existir, ele cria o arquivo sistema.db)
conn = sqlite3.connect('sistema_gestao.db')
cursor = conn.cursor()

# 1. TABELA DE PRODUTOS (Estoque)
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    codigo_barras TEXT UNIQUE,
    preco_custo REAL,
    preco_venda REAL,
    estoque_atual REAL DEFAULT 0
)
''')

# 2. TABELA DE CLIENTES (Para controle de Haver e Contas)
cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf_cnpj TEXT UNIQUE,
    saldo_haver REAL DEFAULT 0 -- Dinheiro que o cliente tem como crédito
)
''')

# 3. TABELA DE VENDAS
cursor.execute('''
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
    valor_total REAL,
    status TEXT, -- 'pago', 'pendente', 'devolvido'
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
)
''')

# 4. TABELA DE CONTAS A RECEBER
cursor.execute('''
CREATE TABLE IF NOT EXISTS contas_a_receber (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_id INTEGER,
    valor_parcela REAL,
    data_vencimento DATE,
    pago BOOLEAN DEFAULT 0,
    FOREIGN KEY (venda_id) REFERENCES vendas(id)
)
''')

# 5. TABELA DE ENTREGAS
cursor.execute('''
CREATE TABLE IF NOT EXISTS entregas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_id INTEGER,
    endereco TEXT NOT NULL,
    entregador TEXT,
    status TEXT DEFAULT 'Pendente', -- 'Pendente', 'Em trânsito', 'Entregue'
    data_saida DATETIME,
    FOREIGN KEY (venda_id) REFERENCES vendas(id)
)
''')

# 6. TABELA DE USUÁRIOS
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
''')

import sqlite3
conn = sqlite3.connect('sistema_gestao.db')
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE contas_a_receber ADD COLUMN forma_pagamento TEXT")
    conn.commit()
    print("Coluna de pagamento adicionada!")
except:
    print("A coluna já existe.")
conn.close()

# Criar um usuário padrão se não existir (Login: admin / Senha: 123)
cursor.execute('INSERT OR IGNORE INTO usuarios (usuario, senha) VALUES ("admin", "123")')

conn.commit()
conn.close()
print("Banco de Dados e tabelas criados com sucesso!")