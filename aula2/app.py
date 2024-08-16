# Bibliotecas
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Configurações
app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///academico.db'
db = SQLAlchemy(app)

# Modelo do banco de dados
class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)
    professor = db.Column(db.String(100), nullable=False)

# Rota inicial
@app.route('/')
def index():
    disciplinas = Disciplina.query.all()
    return render_template('index.html', disciplinas=disciplinas)

# Rota para adicionar
@app.route('/add', methods=['GET', 'POST'])
def add_disciplina():
    if request.method == 'POST':
        nome = request.form['nome']
        carga_horaria = request.form.get('carga_horaria', type=int)
        professor = request.form['professor']
        disciplina = Disciplina(nome=nome, carga_horaria=carga_horaria, professor=professor)
        db.session.add(disciplina)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# Rota para editar
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_disciplina(id):
    disciplina = Disciplina.query.get_or_404(id)
    if request.method == 'POST':
        disciplina.nome = request.form['nome']
        disciplina.carga_horaria = request.form.get('carga_horaria', type=int)
        disciplina.professor = request.form['professor']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', disciplina=disciplina)

# Rota para excluir
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_disciplina(id):
    disciplina = Disciplina.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(disciplina)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete.html', disciplina=disciplina)

# Iniciar a aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)