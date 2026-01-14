import xml.etree.ElementTree as ET
import sqlite3
import os

def importar_xml_para_estoque(caminho_arquivo):
    # Isso descobre em qual pasta este script está rodando agora
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_xml = os.path.join(diretorio_atual, 'teste_nota.xml')
    caminho_db = os.path.join(diretorio_atual, 'sistema_gestao.db')

    # Criar o arquivo de teste automaticamente para garantir que ele exista
    conteudo_teste = """<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">
    <NFe><infNFe><det nItem="1"><prod>
    <cProd>123</cProd><xProd>TECLADO GAMER RGB</xProd><qCom>10.00</qCom><vUnCom>85.00</vUnCom>
    </prod></det></infNFe></NFe></nfeProc>"""
    
    with open(caminho_xml, "w", encoding="utf-8") as f:
        f.write(conteudo_teste)

    # Processar o XML
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    tree = ET.parse(caminho_arquivo)
    root = tree.getroot()

    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()

    for det in root.findall('.//nfe:det', ns):
        nome = det.find('.//nfe:xProd', ns).text
        codigo = det.find('.//nfe:cProd', ns).text
        quantidade = float(det.find('.//nfe:qCom', ns).text)
        preco_custo = float(det.find('.//nfe:vUnCom', ns).text)
        
        try:
            cursor.execute('''
                INSERT INTO produtos (nome, codigo_barras, preco_custo, estoque_atual)
                VALUES (?, ?, ?, ?)
            ''', (nome, codigo, preco_custo, quantidade))
            print(f"Cadastrado: {nome}")
        except sqlite3.IntegrityError:
            cursor.execute('''
                UPDATE produtos SET estoque_atual = estoque_atual + ? 
                WHERE codigo_barras = ?
            ''', (quantidade, codigo))
            print(f"Estoque atualizado: {nome} (+{quantidade})")

    conn.commit()
    conn.close()
    print("\n--- SUCESSO! Verifique seu GitHub Desktop para ver as mudanças ---")

if __name__ == "__main__":
    importar_xml_para_estoque()