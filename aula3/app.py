# Bibliotecas
from flask import Flask, request, jsonify
from urllib.parse import quote_plus
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Configurações
app = Flask(__name__)

# Carregar as credenciais
with open('config.json') as config_file:
    config = json.load(config_file)

# Configurar as credenciais e URL
usuario = quote_plus(config['usuario'])
senha =   quote_plus(config['senha'])
url = f"mongodb+srv://{usuario}:{senha}@cluster1.tjqkv.mongodb.net/?retryWrites=true&w=majority&appName=cluster1"

# Criar o banco de dados e a coleção
client = MongoClient(url, server_api = ServerApi('1'))
colecao = client['flask']['games']

# Rota para enviar o arquivo json (jogos)
@app.route('/enviar_json', methods = ['POST'])
def enviar_json():
    arquivo = request.files.get('arquivo')

    if not arquivo or not arquivo.filename:
        return jsonify({"erro": "Nenhum arquivo selecionado ou enviado"}), 400

    try:
        dados = json.load(arquivo)    
    except Exception as e:
        return jsonify({"erro": f"Erro ao processar o arquivo: {str(e)}"}), 400

    try:
        if isinstance(dados,list):
            colecao.insert_many(dados)
        else:
            colecao.insert_one(dados)
        return jsonify({"mensagem": "Dados JSON inseridos com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Iniciar a aplicação
if __name__ == '__main__':
    app.run(debug=True)