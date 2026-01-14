import sqlite3

def realizar_venda(produto_id, cliente_id, quantidade, valor_venda):
    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()

    # 1. Verificar se tem estoque suficiente
    cursor.execute('SELECT estoque_atual, nome FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()

    if not produto:
        print("Produto não encontrado!")
        return
    
    estoque_atual, nome_prod = produto

    if estoque_atual < quantidade:
        print(f"Estoque insuficiente! Você tem apenas {estoque_atual} de {nome_prod}")
        return

    # 2. Registrar a venda
    cursor.execute('''
        INSERT INTO vendas (cliente_id, valor_total, status)
        VALUES (?, ?, 'pago')
    ''', (cliente_id, valor_venda * quantidade))
    
    # 3. Baixar o estoque
    novo_estoque = estoque_atual - quantidade
    cursor.execute('UPDATE produtos SET estoque_atual = ? WHERE id = ?', (novo_estoque, produto_id))

    conn.commit()
    conn.close()
    print(f"Venda realizada! {quantidade}x {nome_prod} saíram do estoque.")

# TESTE RÁPIDO
if __name__ == "__main__":
    # Vamos supor que você quer vender o produto ID 1 para o cliente ID 1
    # Se você ainda não cadastrou cliente, o ID 1 pode dar erro de chave estrangeira
    p_id = int(input("ID do produto vendido: "))
    qtd = float(input("Quantidade: "))
    preco = float(input("Preço unitário: "))
    
    realizar_venda(p_id, None, qtd, preco) # None significa venda sem cliente identificado

import sqlite3
from datetime import datetime

def finalizar_venda_multi_itens(carrinho, valor_liquido, desconto_total, forma_pgto):
    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()
    data_hoje = datetime.now().strftime('%Y-%m-%d')

    try:
        # 1. Registra a Venda
        cursor.execute('INSERT INTO vendas (data_venda, valor_total) VALUES (?, ?)', 
                       (data_hoje, valor_liquido))
        venda_id = cursor.lastrowid

        # 2. Registra no Contas a Receber com a forma de pagamento
        cursor.execute('''
            INSERT INTO contas_a_receber (venda_id, valor_parcela, status, forma_pagamento)
            VALUES (?, ?, ?, ?)
        ''', (venda_id, valor_liquido, 'Recebido', forma_pgto))

        # 3. Baixa no Estoque
        for item in carrinho:
            cursor.execute('UPDATE produtos SET estoque_atual = estoque_atual - ? WHERE id = ?', 
                           (item['qtd'], item['id']))
            
        conn.commit()
        return True, f"Venda em {forma_pgto} finalizada!"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()