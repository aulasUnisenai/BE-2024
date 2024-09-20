# Bibliotecas
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from extensions import db
from models import Usuario

# Definir rota de autenticação
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Rota de login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.inicial'))
    
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(nome_usuario=nome_usuario).first()
        
        if usuario and usuario.checar_senha(senha):
            login_user(usuario)
            return redirect(url_for('main.inicial'))
        
        flash('Login inválido. Verifique o nome de usuário e/ou a senha.', 'erro')  
    return render_template('login.html')

# Rota de registro
@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('main.inicial'))
    
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        email = request.form['email']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)
        usuario = Usuario(nome_usuario=nome_usuario, email=email, senha=senha_hash)
        
        try:
            db.session.add(usuario)
            db.session.commit()
            flash('Sua conta foi criada! Você agora pode fazer login.', 'sucesso')  # Mensagem de sucesso
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
            flash('Erro ao criar a conta. Nome de usuário ou e-mail já existe.', 'erro')  # Mensagem de erro
    
    return render_template('register.html')

# Rota de logout
@bp.route('/sair')
@login_required
def sair():
    logout_user()
    return redirect(url_for('auth.confirmacao_logout'))

# Rota de confirmação de logout
@bp.route('/confirmacao_logout')
def confirmacao_logout():
    return render_template('confirmacao_logout.html')

# Rota do perfil
@bp.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')