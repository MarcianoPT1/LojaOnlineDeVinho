from tkinter import *
from tkinter import messagebox, filedialog
import sqlite3
import os

janela = Tk()

conn = sqlite3.connect('loja_vinhos.db')
cursor = conn.cursor()

# Adicionar campo de imagem na tabela de vinhos, se não existir
try:
    cursor.execute('''ALTER TABLE vinhos ADD COLUMN imagem TEXT''')
except sqlite3.OperationalError:
    pass  # O campo já existe

# Tabela dos Vinhos
cursor.execute('''CREATE TABLE IF NOT EXISTS vinhos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    marca TEXT NOT NULL,
                    preco REAL NOT NULL,
                    regiao TEXT NOT NULL,
                    ano INTEGER NOT NULL,
                    descricao TEXT NOT NULL,
                    imagem TEXT)
                   ''')
conn.commit()

# Tabela de Utilizadores
cursor.execute('''CREATE TABLE IF NOT EXISTS utilizadores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_utilizador TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    data_nascimento DATE NOT NULL,
                    morada1 TEXT NOT NULL,
                    morada2 TEXT NOT NULL)
                    ''')
conn.commit()

# Tabela de Vendas
cursor.execute('''CREATE TABLE IF NOT EXISTS vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vinho_id INTEGER NOT NULL,
                    utilizador_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    morada1 TEXT NOT NULL,
                    morada2 TEXT NOT NULL)
                    ''')
conn.commit()

# Tabela de Carrinho
cursor.execute('''CREATE TABLE IF NOT EXISTS carrinho (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    utilizador_id INTEGER NOT NULL,
                    vinho_id INTEGER NOT NULL,
                    quantidade INTEGER NOT NULL,
                    FOREIGN KEY (utilizador_id) REFERENCES utilizadores(id),
                    FOREIGN KEY (vinho_id) REFERENCES vinhos(id))
                    ''')
conn.commit()

# Funções para manipulação da base de dados
def inserir_vinho(nome, marca, preco, regiao, ano, descricao):
    cursor.execute('''INSERT INTO vinhos (nome, marca, preco, regiao, ano, descricao)
                      VALUES (?, ?, ?, ?, ?, ?)''', (nome, marca, preco, regiao, ano, descricao))
    conn.commit()

def atualizar_vinho(id, nome, marca, preco, regiao, ano, descricao):
    cursor.execute('''UPDATE vinhos SET nome=?, marca=?, preco=?, regiao=?, ano=?, descricao=?
                      WHERE id=?''', (nome, marca, preco, regiao, ano, descricao, id))
    conn.commit()

def excluir_vinho(id):
    cursor.execute('''DELETE FROM vinhos WHERE id=?''', (id,))
    conn.commit()