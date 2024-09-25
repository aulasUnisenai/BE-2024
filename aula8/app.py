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

# Configurações para o painel do Admin
admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(UserView(User, db.session))
admin.add_link(LogoutMenuLink(name='Logout', endpoint='logout'))
admin.add_link(MenuLink('Gráfico de Usuários', endpoint='users_chart'))


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