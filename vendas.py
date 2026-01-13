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