import os
# Importando as funções dos arquivos que criamos
from leitor_xml import importar_xml_para_estoque
from consultas import buscar_produto
from vendas import realizar_venda
from logistica import agendar_entrega
from relatorios import visualizar_contas_a_receber, baixar_pagamento

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    while True:
        limpar_tela()
        print("="*30)
        print("   SISTEMA DE GESTÃO ERP   ")
        print("="*30)
        print("[1] Lançar XML (Entrada)")
        print("[2] Consultar Estoque / Preços")
        print("[3] Realizar Venda")
        print("[4] Ver/Agendar Entregas")
        print("[5] Relatorio Financeiro / Baixar Pagamento")
        print("[0] Sair")
        print("-"*30)
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            arquivo = input("Nome do arquivo XML (ex: teste_nota.xml): ")
            importar_xml_para_estoque(arquivo)
            input("\nPresione Enter para voltar...")

        elif opcao == '2':
            termo = input("Digite o nome ou código de barras: ")
            # Aqui usamos a função de busca que você já tem
            produtos = buscar_produto(termo)
            for p in produtos:
                print(f"ID: {p[0]} | {p[1]} | Estoque: {p[3]} | Preço: R${p[4]}")
            input("\nPresione Enter para voltar...")

        elif opcao == '3':
            p_id = int(input("ID do Produto: "))
            qtd = float(input("Quantidade: "))
            valor = float(input("Preço Unitário: "))
            realizar_venda(p_id, None, qtd, valor)
            
            entrega = input("Deseja agendar entrega? (s/n): ")
            if entrega.lower() == 's':
                end = input("Endereço de entrega: ")
                agendar_entrega(p_id, end) # Simplificado para o exemplo
            input("\nPresione Enter para voltar...")
        
        elif opcao == '5':
            visualizar_contas_a_receber()
            sub_op = input("\nDeseja baixar algum pagamento? (Digite o ID ou 'n' para sair): ")
            if sub_op.lower() != 'n':
                baixar_pagamento(int(sub_op))
            input("\nPresione Enter para voltar...")
        
         elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")
            input()

if __name__ == "__main__":
    menu()

from auth import fazer_login

# ... (mantenha suas outras funções e o def menu() aqui)

if __name__ == "__main__":
    # O sistema só entra no menu se o login retornar True
    if fazer_login():
        input("Pressione Enter para acessar o painel...")
        menu()
    else:
        print("Sistema encerrado por falta de permissão.")