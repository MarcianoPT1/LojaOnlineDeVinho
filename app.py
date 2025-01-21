import os
import csv
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Chave secreta para sessões

# Conexão com a base de dados
conn = sqlite3.connect('loja_vinhos.db', check_same_thread=False)
cursor = conn.cursor()


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'admin':  # Substitua 'adminpassword' pela palavra-passe desejada
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Palavra-passe inválida!"
    return render_template('admin_login.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    cursor.execute('SELECT * FROM vinhos')
    vinhos = cursor.fetchall()

    cursor.execute('SELECT id, vinho_id, utilizador_id, date, quantidade FROM vendas ORDER BY date')
    vendas = cursor.fetchall()

    return render_template('admin_dashboard.html', vinhos=vinhos, vendas=vendas)


@app.route('/admin/exportar-vendas')
def exportar_vendas():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    cursor.execute('SELECT id, vinho_id, utilizador_id, date, quantidade FROM vendas ORDER BY date')
    vendas = cursor.fetchall()

    # Criar o arquivo CSV
    csv_path = os.path.join(app.root_path, 'vendas.csv')
    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['ID', 'ID do Vinho', 'ID do Utilizador', 'Data', 'Quantidade'])
        for venda in vendas:
            csvwriter.writerow(venda)

    return send_file(csv_path, as_attachment=True)

@app.route('/admin/register-wine', methods=['GET', 'POST'])
def register_wine():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        marca = request.form['marca']
        regiao = request.form['regiao']
        ano = request.form['ano']
        descricao = request.form['descricao']

        cursor.execute('''INSERT INTO vinhos (nome, preco, marca, regiao, ano, descricao)
                          VALUES (?, ?, ?, ?, ?, ?)''', (nome, preco, marca, regiao, ano, descricao))
        conn.commit()

        return redirect(url_for('admin_dashboard'))
    return render_template('admin_wine_register.html')


@app.route('/admin/update-wine', methods=['GET', 'POST'])
def update_wine():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        id = request.form['id']
        nome = request.form['nome']
        preco = request.form['preco']
        marca = request.form['marca']
        regiao = request.form['regiao']
        ano = request.form['ano']
        descricao = request.form['descricao']

        cursor.execute('''UPDATE vinhos SET nome=?, preco=?, marca=?, regiao=?, ano=?, descricao=?
                          WHERE id=?''', (nome, preco, marca, regiao, ano, descricao, id))
        conn.commit()

        return redirect(url_for('admin_dashboard'))
    else:
        id = request.args.get('id')
        cursor.execute('SELECT * FROM vinhos WHERE id=?', (id,))
        vinho = cursor.fetchone()
        return render_template('update_wine.html', vinho=vinho)


@app.route('/admin/confirm-delete-wine', methods=['GET'])
def confirm_delete_wine():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    id = request.args.get('id')
    cursor.execute('SELECT * FROM vinhos WHERE id=?', (id,))
    vinho = cursor.fetchone()
    return render_template('confirm_delete.html', vinho=vinho)


@app.route('/admin/delete-wine', methods=['POST'])
def delete_wine():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    id = request.form['id']
    cursor.execute('DELETE FROM vinhos WHERE id=?', (id,))
    conn.commit()

    return redirect(url_for('admin_dashboard'))


@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    if 'user_id' in session:
        utilizador_id = session['user_id']
        cursor.execute('SELECT morada1, morada2 FROM utilizadores WHERE id=?', (utilizador_id,))
        utilizador = cursor.fetchone()
        morada1, morada2 = utilizador[0], utilizador[1]

        cursor.execute('''SELECT vinho_id, quantidade FROM carrinho WHERE utilizador_id=?''', (utilizador_id,))
        itens_carrinho = cursor.fetchall()

        for item in itens_carrinho:
            vinho_id, quantidade = item
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''INSERT INTO vendas (vinho_id, utilizador_id, date, quantidade, morada1, morada2)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (vinho_id, utilizador_id, date, quantidade, morada1, morada2))

        # Limpar o carrinho após finalizar a compra
        cursor.execute('DELETE FROM carrinho WHERE utilizador_id=?', (utilizador_id,))
        conn.commit()

        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' in session:
        utilizador_id = session['user_id']
        if request.method == 'POST':
            nome_utilizador = request.form['nome_utilizador']
            email = request.form['email']
            data_nascimento = request.form['data_nascimento']
            morada1 = request.form['morada1']
            morada2 = request.form['morada2']
            cursor.execute('''UPDATE utilizadores SET nome_utilizador=?, email=?, data_nascimento=?, morada1=?, morada2=?
                              WHERE id=?''',
                           (nome_utilizador, email, data_nascimento, morada1, morada2, utilizador_id))
            conn.commit()
            return redirect(url_for('home'))
        else:
            cursor.execute('SELECT * FROM utilizadores WHERE id=?', (utilizador_id,))
            utilizador = cursor.fetchone()
            return render_template('settings.html', utilizador=utilizador)
    else:
        return redirect(url_for('login'))


@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' in session:
        utilizador_id = session['user_id']
        cursor.execute('DELETE FROM utilizadores WHERE id=?', (utilizador_id,))
        conn.commit()
        session.pop('user_id', None)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/')
def home():
    cursor.execute('SELECT * FROM vinhos')
    vinhos = cursor.fetchall()
    logged_in = 'user_id' in session
    return render_template('catalog.html', vinhos=vinhos, logged_in=logged_in)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute('SELECT * FROM utilizadores WHERE email=? AND password=?', (email, password))
        utilizador = cursor.fetchone()
        if utilizador:
            session['user_id'] = utilizador[0]
            return redirect(url_for('home'))
        else:
            return "Credenciais inválidas!"
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome_utilizador = request.form['nome_utilizador']
        email = request.form['email']
        password = request.form['password']
        data_nascimento = request.form['data_nascimento']
        morada1 = request.form['morada1']
        morada2 = request.form['morada2']
        cursor.execute('''INSERT INTO utilizadores (nome_utilizador, email, password, data_nascimento, morada1, morada2)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (nome_utilizador, email, password, data_nascimento, morada1, morada2))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/add_to_cart/<int:vinho_id>')
def add_to_cart(vinho_id):
    if 'user_id' in session:
        utilizador_id = session['user_id']
        cursor.execute('''INSERT INTO carrinho (utilizador_id, vinho_id, quantidade)
                          VALUES (?, ?, ?)''', (utilizador_id, vinho_id, 1))
        conn.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/remove_from_cart/<int:vinho_id>')
def remove_from_cart(vinho_id):
    if 'user_id' in session:
        utilizador_id = session['user_id']
        cursor.execute('''DELETE FROM carrinho WHERE utilizador_id=? AND vinho_id=?''', (utilizador_id, vinho_id))
        conn.commit()
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('login'))

@app.route('/cart')
def cart():
    if 'user_id' in session:
        utilizador_id = session['user_id']
        cursor.execute('''SELECT vinhos.nome, vinhos.preco, carrinho.quantidade, vinhos.id
                          FROM carrinho
                          JOIN vinhos ON carrinho.vinho_id = vinhos.id
                          WHERE carrinho.utilizador_id = ?''', (utilizador_id,))
        itens_carrinho = cursor.fetchall()
        return render_template('cart.html', itens_carrinho=itens_carrinho)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)