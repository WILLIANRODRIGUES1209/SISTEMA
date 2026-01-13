import sqlite3
from datetime import datetime

def agendar_entrega(venda_id, endereco):
    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO entregas (venda_id, endereco) VALUES (?, ?)', (venda_id, endereco))
    conn.commit()
    conn.close()
    print(f"Entrega da venda #{venda_id} agendada para: {endereco}")

def atualizar_status_entrega(entrega_id, novo_status, entregador=None):
    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()
    
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        UPDATE entregas 
        SET status = ?, entregador = ?, data_saida = ? 
        WHERE id = ?
    ''', (novo_status, entregador, agora, entrega_id))
    
    conn.commit()
    conn.close()
    print(f"Entrega #{entrega_id} atualizada para: {novo_status}")