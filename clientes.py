import sqlite3

def cadastrar_cliente(nome, cpf):
    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clientes (nome, cpf_cnpj) VALUES (?, ?)', (nome, cpf))
    conn.commit()
    conn.close()
    print(f"Cliente {nome} cadastrado!")