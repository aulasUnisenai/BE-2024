# Bibliotecas
from flask import Blueprint, render_template
from flask_login import login_required

# Rota principal
bp = Blueprint('main', __name__)

# Rota inicial
@bp.route('/')
@login_required
def inicial():
    return render_template('home.html')