from flask import Flask, render_template, request, redirect, url_for, session
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
            return redirect(url_for('register_wine'))
        else:
            return "Palavra-passe inválida!"
    return render_template('admin_login.html')

@app.route('/admin/register-wine', methods=['GET', 'POST'])
def register_wine():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        # Process the form data and add to database
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_wine_register.html')

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
                          VALUES (?, ?, ?, ?, ?, ?)''', (nome_utilizador, email, password, data_nascimento, morada1, morada2))
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