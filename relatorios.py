import sqlite3

def visualizar_contas_a_receber():
    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()
    
    # O SQL abaixo junta a tabela de contas com a de vendas para sabermos o valor
    query = '''
    SELECT cr.id, v.id, cr.valor_parcela, cr.data_vencimento, cr.pago 
    FROM contas_a_receber cr
    JOIN vendas v ON cr.venda_id = v.id
    WHERE cr.pago = 0
    ORDER BY cr.data_vencimento ASC
    '''
    
    cursor.execute(query)
    contas = cursor.fetchall()
    
    print("\n--- CONTAS A RECEBER (PENDENTES) ---")
    print(f"{'ID':<5} | {'Venda':<7} | {'Valor':<10} | {'Vencimento':<12}")
    print("-" * 45)
    
    total_pendente = 0
    for conta in contas:
        status_pago = "Sim" if conta[4] else "Não"
        print(f"{conta[0]:<5} | {conta[1]:<7} | R$ {conta[2]:<7.2f} | {conta[3]:<12}")
        total_pendente += conta[2]
        
    print("-" * 45)
    print(f"TOTAL A RECEBER: R$ {total_pendente:.2f}")
    
    conn.close()

def baixar_pagamento(conta_id):
    """Marca uma parcela como paga"""
    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE contas_a_receber SET pago = 1 WHERE id = ?', (conta_id,))
    conn.commit()
    conn.close()
    print(f"\nPagamento da conta #{conta_id} registrado com sucesso!")