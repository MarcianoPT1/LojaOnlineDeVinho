from tkinter import *
from tkinter import messagebox
import sqlite3

# Conexão com a base de dados
conn = sqlite3.connect('loja_vinhos.db')
cursor = conn.cursor()

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

# Função para adicionar vinho
def adicionar_vinho():
    nome = entry_nome.get()
    marca = entry_marca.get()
    preco = float(entry_preco.get())
    regiao = entry_regiao.get()
    ano = int(entry_ano.get())
    descricao = entry_descricao.get()
    inserir_vinho(nome, marca, preco, regiao, ano, descricao)
    messagebox.showinfo("Sucesso", "Vinho adicionado com sucesso!")

# Função para atualizar vinho
def atualizar_vinho_interface():
    id = int(entry_id.get())
    nome = entry_nome.get()
    marca = entry_marca.get()
    preco = float(entry_preco.get())
    regiao = entry_regiao.get()
    ano = int(entry_ano.get())
    descricao = entry_descricao.get()
    atualizar_vinho(id, nome, marca, preco, regiao, ano, descricao)
    messagebox.showinfo("Sucesso", "Vinho atualizado com sucesso!")

# Função para excluir vinho
def excluir_vinho_interface():
    id = int(entry_id.get())
    excluir_vinho(id)
    messagebox.showinfo("Sucesso", "Vinho excluído com sucesso!")

# Interface Tkinter
janela = Tk()
janela.title("Gestão de Vinhos")

# Campos de entrada
Label(janela, text="ID").grid(row=0, column=0)
entry_id = Entry(janela)
entry_id.grid(row=0, column=1)

Label(janela, text="Nome").grid(row=1, column=0)
entry_nome = Entry(janela)
entry_nome.grid(row=1, column=1)

Label(janela, text="Marca").grid(row=2, column=0)
entry_marca = Entry(janela)
entry_marca.grid(row=2, column=1)

Label(janela, text="Preço").grid(row=3, column=0)
entry_preco = Entry(janela)
entry_preco.grid(row=3, column=1)

Label(janela, text="Região").grid(row=4, column=0)
entry_regiao = Entry(janela)
entry_regiao.grid(row=4, column=1)

Label(janela, text="Ano").grid(row=5, column=0)
entry_ano = Entry(janela)
entry_ano.grid(row=5, column=1)

Label(janela, text="Descrição").grid(row=6, column=0)
entry_descricao = Entry(janela)
entry_descricao.grid(row=6, column=1)

# Botões
Button(janela, text="Adicionar Vinho", command=adicionar_vinho).grid(row=7, column=0)
Button(janela, text="Atualizar Vinho", command=atualizar_vinho_interface).grid(row=7, column=1)
Button(janela, text="Excluir Vinho", command=excluir_vinho_interface).grid(row=7, column=2)

janela.mainloop()