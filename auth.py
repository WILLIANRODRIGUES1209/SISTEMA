import sqlite3

def fazer_login():
    print("\n" + "="*30)
    print("      ACESSO RESTRITO")
    print("="*30)
    
    usuario_input = input("Usuário: ")
    senha_input = input("Senha: ")

    conn = sqlite3.connect('sistema_gestao.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM usuarios WHERE usuario = ? AND senha = ?', (usuario_input, senha_input))
    usuario_encontrado = cursor.fetchone()
    
    conn.close()

    if usuario_encontrado:
        print("\n✅ Login realizado com sucesso!")
        return True
    else:
        print("\n❌ Usuário ou senha incorretos!")
        return False