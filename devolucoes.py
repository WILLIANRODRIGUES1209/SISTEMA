import sqlite3

def registrar_devolucao(cliente_id, produto_id, quantidade, valor_unidade):
    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()

    # 1. Aumentar o estoque do produto que está voltando
    cursor.execute('UPDATE produtos SET estoque_atual = estoque_atual + ? WHERE id = ?', 
                   (quantidade, produto_id))

    # 2. Calcular o valor total do crédito
    valor_credito = quantidade * valor_unidade

    # 3. Adicionar esse valor ao "Haver" do cliente
    cursor.execute('UPDATE clientes SET saldo_haver = saldo_haver + ? WHERE id = ?', 
                   (valor_credito, cliente_id))

    conn.commit()
    conn.close()
    print(f"Sucesso! R$ {valor_credito:.2f} adicionados ao crédito do cliente.")