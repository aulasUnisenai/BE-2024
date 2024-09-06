from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Recebendo solicitação...")
    data = request.json
    print("Dados recebidos:", data)
    return jsonify({"mensagem": "Dados recebidos com sucesso!", "dados": data}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Porta 5001 para o webhook