# Bibliotecas
from flask import Flask, request, jsonify
from urllib.parse import quote_plus
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId # trabalhar com o ID 

 # Configurações
app = Flask(__name__)

# Carregar configurações de conexão do MongoDB
with open('config.json') as config_file:
    config = json.load(config_file)

# Configurar credenciais e URI
usuario = quote_plus(config['usuario'])
senha = quote_plus(config['senha'])
uri = f"suaURI"

# Conectar ao MongoDB
cliente = MongoClient(uri, server_api=ServerApi('1'))
colecao = cliente['flask']['games']

# Rota para enviar o JSON
@app.route('/enviar_json', methods=['POST'])
def enviar_json():
    arquivo = request.files.get('arquivo')
    if not arquivo or not arquivo.filename:
        return jsonify({"erro": "Nenhum arquivo selecionado ou enviado"}), 400
    try:
        dados = json.load(arquivo)
    except Exception as e:
        return jsonify({"erro": f"Erro ao processar o arquivo: {str(e)}"}), 400
    try:
        if isinstance(dados, list):
            colecao.insert_many(dados)
        else:
            colecao.insert_one(dados)
        return jsonify({"mensagem": "Dados JSON inseridos com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para consultar os arquivos
@app.route('/consultar_json', methods = ['GET'])
def consultar_json():
    campo = request.args.get('campo')
    valor = request.args.get('valor')
    operador = request.args.get('operador', 'eq')

    if not campo or not valor:
        return jsonify({"erro": "Campo e valor são necessários"}), 400
    
    try:
        # Converter valor para tipo adequado
        try:
            valor = float(valor)
        except ValueError:
            pass # Manter como string

        # Construir os operadores
        operadores = {
            'gte': {"$gte": valor},
            'lte': {"$lte": valor},
            'eq': valor
        }
        consulta = {campo: operadores.get(operador, valor)} #query
        documentos = list(colecao.find(consulta))
        for doc in documentos:
            doc['_id']= str(doc['_id']) # Converter ObjectId em string
        return jsonify(documentos), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para atualizar documentos
@app.route('/atualizar_json', methods =['PUT'])
def atualizar_documento():
    try:
        # Verificar se um ID foi fornecido
        id = request.args.get('id')
        criterio = {}

        if id:
            if not ObjectId.is_valid(id):
                return jsonify({"erro": "ID inválido"}), 400
            criterio["_id"] = ObjectId(id)
        else:
            # Se não for fornecido um ID
            criterio = request.json.get('criterio', {})
        
        # Obter os dados do corpo da requisição
        dados_atualizados = request.json.get('dados_atualizados', {})
        if not dados_atualizados:
            return jsonify({"erro": "Nenhum dado fornecido para atualização"}), 400
        
        # Atualizar os documentos
        resultado = colecao.update_many(criterio, {"$set":dados_atualizados})

        if resultado.matched_count == 0:
            return jsonify({"erro": "Nenhum documento encontrado com os critérios fornecidos"}), 404
        
        return jsonify({
            "mensagem": "Documentos atualizados com sucesso!",
            "documentos_atualizados": resultado.modified_count
        }), 200
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para deletar os documentos
@app.route("/deletar_json", methods =["DELETE"])
def deletar_json():
    try:
        id = request.args.get('id')
        criterio = {}

        if id:
            if not ObjectId.is_valid(id):
                return jsonify({"erro": "ID inválido"}), 400
            criterio['_id'] = ObjectId(id)
        
        else:
            criterio = request.json.get('criterio', {})

        resultado = colecao.delete_many(criterio)

        if resultado.deleted_count == 0:
            return jsonify({"erro": "Nenhum documento encontrado com os critérios fornecidos"}), 404
        
        return  jsonify({
            "mensagem": "Documentos deletados com sucesso",
            "documentos_deletados": resultado.deleted_count
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Iniciar a aplicação
if __name__ == '__main__':
    app.run(debug=True)