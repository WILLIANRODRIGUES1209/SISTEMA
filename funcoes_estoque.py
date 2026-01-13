import sqlite3

def cadastrar_produto(nome, codigo_barras, preco_custo, preco_venda, estoque_inicial):
    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO produtos (nome, codigo_barras, preco_custo, preco_venda, estoque_atual)
        VALUES (?, ?, ?, ?, ?)
        ''', (nome, codigo_barras, preco_custo, preco_venda, estoque_inicial))
        
        conn.commit()
        print(f"Produto '{nome}' cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Este código de barras já está cadastrado!")
    finally:
        conn.close()

# TESTE: Vamos cadastrar um produto agora
if __name__ == "__main__":
    nome_prod = input("Nome do produto: ")
    cod_barras = input("Código de barras: ")
    custo = float(input("Preço de custo: "))
    venda = float(input("Preço de venda: "))
    qtd = float(input("Quantidade inicial: "))
    
    cadastrar_produto(nome_prod, cod_barras, custo, venda, qtd)