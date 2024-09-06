from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pedidos.db'
db = SQLAlchemy(app)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_pedido = db.Column(db.String(50), nullable=False)
    nome_produto = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)

# URL do webhook externo
WEBHOOK_URL = 'http://localhost:5001/webhook'  # URL do webhook local

# Rota para renderizar o formulário de cadastro de pedido
@app.route('/')
def inicio():
    return render_template('index.html')

# Rota para receber os dados do formulário via POST
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    numero_pedido = request.form.get('numero_pedido')
    nome_produto = request.form.get('nome_produto')
    quantidade = int(request.form.get('quantidade'))
    preco = float(request.form.get('preco'))
    status = request.form.get('status')

    # Calcula o total da compra
    total = quantidade * preco

    # Cria um novo pedido
    novo_pedido = Pedido(numero_pedido=numero_pedido, nome_produto=nome_produto, quantidade=quantidade, preco=preco, total=total, status=status)
    db.session.add(novo_pedido)
    db.session.commit()

    # Envia dados do pedido para o webhook externo
    payload = {
        'numero_pedido': numero_pedido,
        'nome_produto': nome_produto,
        'quantidade': quantidade,
        'preco': preco,
        'total': total,
        'status': status
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()  # Levanta um erro se a requisição falhar
    except requests.RequestException as e:
        print(f'Erro ao enviar webhook: {e}')

    return jsonify({'mensagem': 'Pedido cadastrado com sucesso.'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)