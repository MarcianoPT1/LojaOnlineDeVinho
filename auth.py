import sqlite3

# Conexão com a base de dados
conn = sqlite3.connect('loja_vinhos.db')
cursor = conn.cursor()

# Função para registrar utilizador
def registrar_utilizador(nome_utilizador, email, password, data_nascimento, morada1, morada2):
    cursor.execute('''INSERT INTO utilizadores (nome_utilizador, email, password, data_nascimento, morada1, morada2)
                      VALUES (?, ?, ?, ?, ?, ?)''', (nome_utilizador, email, password, data_nascimento, morada1, morada2))
    conn.commit()

# Função para autenticar utilizador
def autenticar_utilizador(email, password):
    cursor.execute('''SELECT * FROM utilizadores WHERE email=? AND password=?''', (email, password))
    utilizador = cursor.fetchone()
    if utilizador:
        return True
    return False