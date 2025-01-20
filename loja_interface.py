import tkinter as tk
from tkinter import messagebox
import sqlite3


class LojaVinhos:
    """
    Interface gráfica simples para uma loja de vinhos.
    Permite visualizar vinhos, fazer login e gerir um carrinho de compras.
    """

    def __init__(self):
        # Inicialização da janela principal
        self.janela = tk.Tk()
        self.janela.title("Loja de Vinhos")
        self.janela.geometry("600x400")

        # Conexão à base de dados
        self.conn = sqlite3.connect('loja_vinhos.db')
        self.cursor = self.conn.cursor()

        # Variável para guardar o ID do utilizador atual
        self.utilizador_atual = None

        # Criar a área principal PRIMEIRO
        self.area_principal = tk.Frame(self.janela)
        self.area_principal.pack(expand=True, fill='both', padx=10, pady=10)

        # DEPOIS criar o menu e mostrar o catálogo
        self.criar_menu()
        self.mostrar_catalogo()

    def criar_menu(self):
        """
        Cria a barra de menu principal com as opções básicas.
        """
        # Frame para o menu
        menu_frame = tk.Frame(self.janela, bg='lightgray')
        menu_frame.pack(fill='x')

        # Botões do menu
        tk.Button(menu_frame, text="Catálogo", command=self.mostrar_catalogo).pack(side='left', padx=5, pady=5)
        tk.Button(menu_frame, text="Carrinho", command=self.mostrar_carrinho).pack(side='left', padx=5, pady=5)
        tk.Button(menu_frame, text="Login", command=self.mostrar_login).pack(side='right', padx=5, pady=5)

    def criar_area_principal(self):
        """
        Cria a área principal onde será mostrado o conteúdo.
        """
        self.area_principal = tk.Frame(self.janela)
        self.area_principal.pack(expand=True, fill='both', padx=10, pady=10)

        # Mostrar o catálogo por defeito
        self.mostrar_catalogo()

    def limpar_area_principal(self):
        """
        Limpa todos os elementos da área principal.
        """
        for widget in self.area_principal.winfo_children():
            widget.destroy()

    def mostrar_catalogo(self):
        """
        Mostra a lista de vinhos disponíveis.
        """
        self.limpar_area_principal()

        # Título
        tk.Label(self.area_principal, text="Catálogo de Vinhos", font=('Arial', 14, 'bold')).pack(pady=10)

        # Lista de vinhos
        self.cursor.execute('SELECT id, nome, marca, preco FROM vinhos')
        vinhos = self.cursor.fetchall()

        # Frame para a lista
        lista_frame = tk.Frame(self.area_principal)
        lista_frame.pack(fill='both', expand=True)

        # Cabeçalho
        tk.Label(lista_frame, text="ID", width=5).grid(row=0, column=0, padx=5)
        tk.Label(lista_frame, text="Nome", width=20).grid(row=0, column=1, padx=5)
        tk.Label(lista_frame, text="Marca", width=15).grid(row=0, column=2, padx=5)
        tk.Label(lista_frame, text="Preço", width=10).grid(row=0, column=3, padx=5)

        # Adicionar vinhos à lista
        for i, vinho in enumerate(vinhos, 1):
            tk.Label(lista_frame, text=str(vinho[0])).grid(row=i, column=0, padx=5)
            tk.Label(lista_frame, text=vinho[1]).grid(row=i, column=1, padx=5)
            tk.Label(lista_frame, text=vinho[2]).grid(row=i, column=2, padx=5)
            tk.Label(lista_frame, text=f"€{vinho[3]:.2f}").grid(row=i, column=3, padx=5)

            # Botão para adicionar ao carrinho
            if self.utilizador_atual:
                tk.Button(
                    lista_frame,
                    text="Adicionar",
                    command=lambda v=vinho[0]: self.adicionar_ao_carrinho(v)
                ).grid(row=i, column=4, padx=5)

    def mostrar_carrinho(self):
        """
        Mostra o carrinho de compras do utilizador atual.
        """
        self.limpar_area_principal()

        if not self.utilizador_atual:
            tk.Label(self.area_principal, text="Por favor, faça login primeiro").pack(pady=20)
            return

        # Título
        tk.Label(self.area_principal, text="Carrinho de Compras", font=('Arial', 14, 'bold')).pack(pady=10)

        # Buscar items do carrinho
        self.cursor.execute('''
            SELECT v.nome, v.preco, c.quantidade
            FROM carrinho c
            JOIN vinhos v ON c.vinho_id = v.id
            WHERE c.utilizador_id = ?
        ''', (self.utilizador_atual,))

        items = self.cursor.fetchall()

        if not items:
            tk.Label(self.area_principal, text="Carrinho vazio").pack(pady=20)
            return

        # Lista de items
        for item in items:
            frame = tk.Frame(self.area_principal)
            frame.pack(fill='x', pady=5)
            tk.Label(frame, text=item[0], width=20).pack(side='left')
            tk.Label(frame, text=f"€{item[1]:.2f}", width=10).pack(side='left')
            tk.Label(frame, text=f"Qtd: {item[2]}", width=10).pack(side='left')

    def mostrar_login(self):
        """
        Mostra o formulário de login.
        """
        self.limpar_area_principal()

        # Título
        tk.Label(self.area_principal, text="Login", font=('Arial', 14, 'bold')).pack(pady=10)

        # Formulário
        tk.Label(self.area_principal, text="Email:").pack()
        email = tk.Entry(self.area_principal)
        email.pack()

        tk.Label(self.area_principal, text="Password:").pack()
        password = tk.Entry(self.area_principal, show="*")
        password.pack()

        # Botão de login
        tk.Button(
            self.area_principal,
            text="Entrar",
            command=lambda: self.fazer_login(email.get(), password.get())
        ).pack(pady=10)

    def fazer_login(self, email, password):
        """
        Processa o login do utilizador.

        Args:
            email (str): Email do utilizador
            password (str): Password do utilizador
        """
        self.cursor.execute(
            'SELECT id FROM utilizadores WHERE email=? AND password=?',
            (email, password)
        )
        utilizador = self.cursor.fetchone()

        if utilizador:
            self.utilizador_atual = utilizador[0]
            messagebox.showinfo("Sucesso", "Login efetuado com sucesso!")
            self.mostrar_catalogo()
        else:
            messagebox.showerror("Erro", "Email ou password inválidos")

    def adicionar_ao_carrinho(self, vinho_id):
        """
        Adiciona um vinho ao carrinho.

        Args:
            vinho_id (int): ID do vinho a adicionar
        """
        try:
            self.cursor.execute(
                'INSERT INTO carrinho (utilizador_id, vinho_id, quantidade) VALUES (?, ?, 1)',
                (self.utilizador_atual, vinho_id)
            )
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Vinho adicionado ao carrinho!")
        except sqlite3.Error:
            messagebox.showerror("Erro", "Erro ao adicionar ao carrinho")

    def iniciar(self):
        """
        Inicia a aplicação.
        """
        self.janela.mainloop()


# Criar e iniciar a aplicação
if __name__ == "__main__":
    app = LojaVinhos()
    app.iniciar()