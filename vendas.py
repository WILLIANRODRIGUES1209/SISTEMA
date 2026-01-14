import sqlite3
from datetime import datetime

def finalizar_venda_multi_itens(carrinho, valor_liquido, desconto_total, forma_pgto):
    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()
    data_hoje = datetime.now().strftime('%Y-%m-%d')

    try:
        # 1. Registra a Venda Geral
        cursor.execute('''
            INSERT INTO vendas (data_venda, valor_total) 
            VALUES (?, ?)
        ''', (data_hoje, valor_liquido))
        
        # Pega o ID da venda que acabou de ser criada
        venda_id = cursor.lastrowid

        # 2. Registra no CONTAS A RECEBER (O que estava faltando!)
        # O status 'Recebido' assume que a venda foi paga na hora
        cursor.execute('''
            INSERT INTO contas_a_receber (venda_id, valor_parcela, status, forma_pagamento)
            VALUES (?, ?, ?, ?)
        ''', (venda_id, valor_liquido, 'Recebido', forma_pgto))

        # 3. Baixa cada item no estoque
        for item in carrinho:
            cursor.execute('''
                UPDATE produtos 
                SET estoque_atual = estoque_atual - ? 
                WHERE id = ?
            ''', (item['qtd'], item['id']))
            
        conn.commit()
        return True, "Venda e Financeiro registrados com sucesso!"
    
    except Exception as e:
        conn.rollback() # Se der erro em qualquer passo, ele cancela tudo para não bugar o banco
        return False, f"Erro no banco: {str(e)}"
    finally:
        conn.close()