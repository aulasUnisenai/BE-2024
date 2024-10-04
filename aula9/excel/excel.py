# Bibliotecas
from flask import Flask, render_template, send_file, request, redirect
import pandas as pd
import os
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')

# Definir o caminho absoluto para o arquivo Excel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, 'dados.xlsx')

# Função principal
def raspar_e_salvar():
    url = 'https://pt.wikipedia.org/wiki/Comparação_entre_linguagens_de_programação'

    # Tente realizar o scraping e salvar os dados
    try:
        resposta = requests.get(url)
        resposta.encoding = 'utf-8'  # Garantir que a codificação seja UTF-8
        tabelas = pd.read_html(resposta.text)
        df = pd.DataFrame(tabelas[0]) 

        # Salvar o arquivo Excel no caminho definido
        df.to_excel(FILE_PATH, index=False, engine='openpyxl')
        return True
    except Exception as e:
        return str(e)

# Rota inicial
@app.route('/')
def index():
    mensagem = None
    if request.args.get('saved'):
        mensagem = "Os dados foram salvos em 'dados.xlsx'."
    return render_template('index.html', mensagem=mensagem)

# Rota de download
@app.route('/download')
def baixar_arquivo():
    if os.path.exists(FILE_PATH):
        return send_file(FILE_PATH, as_attachment=True)
    return "O arquivo não está disponível para download."

# Rota para a coleta
@app.route('/scrape')
def raspar():
    resultado = raspar_e_salvar()
    if resultado is True:
        return redirect('/?saved=1')
    else:
        return f"Ocorreu um erro durante o scraping: {resultado}"

# Iniciar aplicação
if __name__ == '__main__':
    app.run(debug=True)