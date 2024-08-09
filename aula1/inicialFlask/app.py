# Bibliotecas e módulos
from flask import Flask, render_template

# Instância do aplicativo
app = Flask(__name__, template_folder='templates', static_folder='static')

# Rota inicial
@app.route("/")
def index():
    message = 'Olá, Mundo!'
    return render_template('index.html', message=message)

# Rota para o conteúdo do professor
@app.route("/professor")
def professor():
    return '<h1>Olá, professor (a)! Seja bem-vindo (a).</h1>'

# Iniciar a aplicação
if __name__ == "__main__":
    app.run(debug=True)