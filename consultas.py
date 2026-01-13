import sqlite3

def buscar_produto(termo):
    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()
    
    # A busca usa o comando LIKE para encontrar nomes parciais
    # E também busca pelo código de barras exato
    query = '''
    SELECT id, nome, codigo_barras, estoque_atual, preco_venda 
    FROM produtos 
    WHERE nome LIKE ? OR codigo_barras = ?
    '''
    
    cursor.execute(query, (f'%{termo}%', termo))
    resultados = cursor.fetchall()
    
    conn.close()
    return resultados

# TESTE DA BUSCA
if __name__ == "__main__":
    busca = input("Digite o nome ou código de barras: ")
    produtos = buscar_produto(busca)
    
    if produtos:
        print(f"\n{'ID':<5} | {'Nome':<20} | {'Estoque':<8} | {'Preço':<10}")
        print("-" * 50)
        for p in produtos:
            print(f"{p[0]:<5} | {p[1]:<20} | {p[3]:<8} | R$ {p[4]:.2f}")
    else:
        print("Nenhum produto encontrado.")