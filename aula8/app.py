# Bibliotecas
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
import logging
import json

# Configurações
app = Flask(__name__, template_folder='templates', static_folder='static')
app.permanent_session_lifetime = timedelta(minutes=2)
app.config['SECRET_KEY'] = 'UNISENAI'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///acesso.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
logging.basicConfig(filename='app.log', level=logging.INFO)

# Classe usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True)
    password_hash = db.Column(db.String(20))
    role = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Classe para a visão do usuário
class UserView(ModelView):
    column_list = ('username', 'email', 'role')
    form_columns = ('username', 'email', 'password', 'role')
    form_extra_fields = {
        'password': PasswordField('Senha', validators=[DataRequired()]),
        'role': SelectField('Função', choices= [('aluno', 'Aluno'),('professor', 'Professor')], validators=[DataRequired()])
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'
    
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.set_password(form.password.data)
        elif form.password.data:
            model.set_password(form.password.data)
        db.session.commit()

# Classe para o formulário de login
class LoginForm(FlaskForm):
    username = StringField('Nome do usuário', validators=[DataRequired(), Length(min = 4, max = 20)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar de mim')

class UserCreationForm(FlaskForm):
    username = StringField('Nome do usuário', validators=[DataRequired(), Length(min = 4, max = 20)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=5)])
    role = SelectField('Papel', choices=[('admin', 'Admin'), ('aluno', 'Aluno'), ('professor', 'Professor')], validators=[DataRequired()])

class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'
    
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role =='admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    
    @expose('/')
    def index(self):
        self._template_args['logout_link'] = LogoutMenuLink('Logout', endpoint= 'logout')
        return super().index()

# Configurações para o painel do Admin
admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(UserView(User, db.session))
admin.add_link(LogoutMenuLink(name='Logout', endpoint='logout'))
admin.add_link(MenuLink('Gráfico de Usuários', endpoint='users_chart'))

# Função para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index') if current_user.role == 'admin' else f'{current_user.role}')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember= form.remember.data)
            session.permanent = True
            logging.info(f'Usuário {user.username} fez login')
            return redirect(url_for('index'))
        flash('Nome de usuário ou senha incorretos', 'danger')
    return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logging.info(f'Usuário {current_user.username} fez logout')
    logout_user()
    return redirect(url_for('login'))

@app.route('/create_user', methods =['POST'])
@login_required
def create_user():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    
    form = UserCreationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data, role = form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('admin.index'))
    
    return render_template('create_user.html', form=form)

@app.route('/professor')
@login_required
def professor():
    if current_user.role == 'professor':
        return render_template('professor.html')
    flash('Acesso negado', 'danger')
    return redirect(url_for('index'))

@app.route('/aluno')
@login_required
def aluno():
    if current_user.role == 'aluno':
        return render_template('aluno.html')
    flash('Acesso negado', 'danger')
    return redirect(url_for('index'))

@app.before_request
def before_request():
    if current_user.is_authenticated:
        now = datetime.now(timezone.utc).astimezone()
        if 'expiration' not in session or session['expiration'] < now:
            session['expiration'] = now + app.permanent_session_lifetime
        session['remaining_time'] = (session['expiration'] - now).seconds //60
    else:
        session.pop('expiration', None)
        session.pop('remaining_time', None)

@app.route('/users_chart')
@login_required
def users_chart():
    if current_user.role != 'admin':
        flash('Acesso negado.', 'danger')
        return redirect(url_for('index'))

    roles = db.session.query(User.role).distinct().all()
    role_counts = db.session.query(User.role, db.func.count(User.id)).group_by(User.role).all()
    
    role_count_dict = {role[0]: 0 for role in roles}
    for role, count in role_counts:
        role_count_dict[role] = count

    labels = list(role_count_dict.keys())
    values = list(role_count_dict.values())

    chart_data = {
        'data': [{
            'x': labels,
            'y': values,
            'type': 'bar',
            'marker': {
                'color': ['#1f77b4', '#ff7f0e', '#2ca02c']  
            },
            'textposition': 'auto',
        }],
        'layout': {
            'title': 'Total de Usuários por Função',
            'template': 'none',
            'height': 300,
            'xaxis': {
                'title': 'Funções',
            },
            'yaxis': {
                'title': 'Número de Usuários',
                'dtick': 1 
            },
        }
    }

    return render_template('users_chart.html', chart_data=json.dumps(chart_data))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(role = 'admin').first():
            admin_user = User(username = 'Admin', email = 'admin@admin.com', role = 'admin')
            admin_user.set_password('admin')
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug= True)