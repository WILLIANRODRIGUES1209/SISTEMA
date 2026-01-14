import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Meu ERP Web", layout="wide")

def carregar_dados(query):
    conn = sqlite3.connect('sistema_gestao.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("🚀 Sistema de Gestão ERP - Web Version")

# Resumo no topo da página
st.subheader("📊 Resumo de Vendas")
dados_vendas = carregar_dados("SELECT data_venda, valor_total FROM vendas")

if not dados_vendas.empty:
    # Cria um gráfico de barras simples com o faturamento por data
    st.bar_chart(dados_vendas.set_index('data_venda'))
else:
    st.info("Nenhuma venda registrada ainda.")

# Menu Lateral
menu = st.sidebar.selectbox("Navegação", ["Estoque", "Vendas", "Financeiro", "Logística"])

if menu == "Estoque":
    st.header("📦 Controle de Estoque")
    
    # Botão de Upload de XML
    arquivo_xml = st.file_uploader("Importar Nota Fiscal (XML)", type=["xml"])
    
    if arquivo_xml is not None:
        # Importamos a função que você já criou
        from leitor_xml import importar_xml_para_estoque
        
        # Salva o arquivo temporariamente para processar
        with open("temp_nota.xml", "wb") as f:
            f.write(arquivo_xml.getbuffer())
        
        # Chama sua lógica de banco de dados
        importar_xml_para_estoque("temp_nota.xml")
        st.success("Nota Fiscal processada e estoque atualizado!")

    # Exibe a tabela atualizada
    produtos = carregar_dados("SELECT id, nome, estoque_atual, preco_custo FROM produtos")
    st.dataframe(produtos, use_container_width=True)
    
    if st.button("Simular Entrada XML"):
        st.info("Aqui você poderá arrastar seu arquivo XML em breve!")

elif menu == "Vendas":
    st.header("🛒 Ponto de Venda (PDV)")

    # Inicializa o carrinho se não existir
    if 'carrinho' not in st.session_state:
        st.session_state.carrinho = []

    # --- BUSCA E SELEÇÃO DE PRODUTOS ---
    with st.expander("🔍 Abrir Catálogo de Produtos", expanded=True):
        produtos_df = carregar_dados("SELECT id, nome, estoque_atual, preco_custo FROM produtos")
        st.dataframe(produtos_df, use_container_width=True)
        
        col_id, col_qnt, col_add = st.columns([1, 1, 1])
        with col_id:
            id_sel = st.number_input("ID do Produto", step=1, key="id_venda")
        with col_qnt:
            qnt_sel = st.number_input("Qtd", min_value=1, value=1, key="qtd_venda")
        with col_add:
            if st.button("➕ Adicionar ao Carrinho"):
                # Busca detalhes do produto selecionado
                prod_info = produtos_df[produtos_df['id'] == id_sel]
                if not prod_info.empty:
                    item = {
                        "id": id_sel,
                        "nome": prod_info.iloc[0]['nome'],
                        "qtd": qnt_sel,
                        "preco_unit": prod_info.iloc[0]['preco_custo'] or 0.0,
                        "subtotal": qnt_sel * (prod_info.iloc[0]['preco_custo'] or 0.0)
                    }
                    st.session_state.carrinho.append(item)
                else:
                    st.error("Produto não encontrado!")

    # --- EXIBIÇÃO DO CARRINHO ---
    if st.session_state.carrinho:
        st.subheader("📋 Itens da Venda")
        df_carrinho = pd.DataFrame(st.session_state.carrinho)
        st.table(df_carrinho)
        
        valor_bruto = df_carrinho['subtotal'].sum()
        
        # --- DESCONTOS ---
        st.divider()
        col_desc1, col_desc2 = st.columns(2)
        with col_desc1:
            tipo_desconto = st.radio("Tipo de Desconto", ["R$ (Valor Fixo)", "% (Porcentagem)"])
        with col_desc2:
            valor_desconto = st.number_input("Valor do Desconto", min_value=0.0)

        # Cálculo do Líquido
        if tipo_desconto == "% (Porcentagem)":
            total_liquido = valor_bruto - (valor_bruto * (valor_desconto / 100))
        else:
            total_liquido = valor_bruto - valor_desconto

        # --- TOTAIS E PAGAMENTO ---
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Bruto", f"R$ {valor_bruto:,.2f}")
        c2.metric("Desconto", f"- R$ {valor_bruto - total_liquido:,.2f}")
        c3.metric("Total Líquido", f"R$ {total_liquido:,.2f}")

        st.divider()
        # Seleção da forma de pagamento
        forma_pgto = st.selectbox(
            "Selecione a Forma de Pagamento",
            ["Dinheiro", "PIX", "Cartão de Crédito", "Cartão de Débito", "Cheque"]
        )

        if st.button("✅ FINALIZAR VENDA", key="btn_finalizar_venda_principal"):
            
            # Passamos agora a forma de pagamento para a função
            sucesso, mensagem = finalizar_venda_multi_itens(
                st.session_state.carrinho, 
                total_liquido, 
                (valor_bruto - total_liquido),
                forma_pgto # Novo argumento
            )
            # ... resto do código de sucesso ...

        if st.button("✅ FINALIZAR VENDA"):
            # Aqui entraria a lógica de salvar no banco e baixar estoque
            st.balloons()
            st.success("Venda realizada com sucesso!")
            st.session_state.carrinho = [] # Limpa o carrinho
    
    if st.button("✅ FINALIZAR VENDA"):
            # Importa a função que acabamos de criar
            from vendas import finalizar_venda_multi_itens
            
            sucesso, mensagem = finalizar_venda_multi_itens(
                st.session_state.carrinho, 
                total_liquido, 
                (valor_bruto - total_liquido)
            )
            
            if sucesso:
                st.balloons()
                st.success(mensagem)
                # Limpa o carrinho após a venda
                st.session_state.carrinho = []
                st.rerun()
            else:
                st.error(mensagem)

elif menu == "Financeiro":
    st.header("📊 Contas a Receber")
    contas = carregar_dados("SELECT * FROM contas_a_receber")
    st.table(contas)

elif menu == "Logística":
    st.header("🚚 Entregas Pendentes")
    entregas = carregar_dados("SELECT * FROM entregas")
    st.write(entregas)

elif menu == "Financeiro":
    st.header("📊 Resumo do Caixa")
    
    # Query que soma por forma de pagamento
    resumo_pagamentos = carregar_dados("""
        SELECT forma_pagamento, SUM(valor_parcela) as total 
        FROM contas_a_receber 
        GROUP BY forma_pagamento
    """)
    
    # Exibe em colunas bonitas
    if not resumo_pagamentos.empty:
        cols = st.columns(len(resumo_pagamentos))
        for i, row in resumo_pagamentos.iterrows():
            cols[i].metric(row['forma_pagamento'], f"R$ {row['total']:,.2f}")
    
    st.divider()
    st.subheader("Lista Detalhada")
    st.dataframe(carregar_dados("SELECT * FROM contas_a_receber"), use_container_width=True)