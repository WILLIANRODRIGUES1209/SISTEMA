import sqlite3
import random

def popular_estoque():
    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()

    # Listas para gerar nomes aleatórios
    prefixos = ["Cabo", "Sensor", "Placa", "Adaptador", "Módulo", "Suporte", "Kit"]
    nomes = ["USB", "Wi-Fi", "Bluetooth", "HDMI", "LED", "de Pressão", "Industrial"]
    marcas = ["Tech", "Premium", "Master", "Flex", "Pro"]

    print("Gerando 20 produtos aleatórios...")

    for _ in range(20):
        nome_prod = f"{random.choice(prefixos)} {random.choice(nomes)} {random.choice(marcas)}"
        codigo_barras = str(random.randint(7890000000000, 7899999999999))
        estoque = float(random.randint(5, 100))
        preco = round(random.uniform(15.0, 450.0), 2)

        cursor.execute('''
            INSERT INTO produtos (nome, codigo_barras, estoque_atual, preco_custo)
            VALUES (?, ?, ?, ?)
        ''', (nome_prod, codigo_barras, estoque, preco))

    conn.commit()
    conn.close()
    print("✅ 20 novas peças foram adicionadas ao seu estoque!")

if __name__ == "__main__":
    popular_estoque()