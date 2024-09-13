# Bibliotecas
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo
import plotly.graph_objs as go
import plotly.io as pio

# Configurações
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monitor.db'
db = SQLAlchemy(app)

# Função para obter o timestamp atual em Brasília
def obter_timestamp_brasilia():
    return datetime.now(ZoneInfo('America/Sao_Paulo'))

# Modelo de dados
class DadosSensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperatura = db.Column(db.Float, nullable=False)
    umidade = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=obter_timestamp_brasilia, nullable=False)

# Rota para página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para visualizar o dashboard
@app.route('/dashboard')
def dashboard():
    # Consultando os dados do banco
    dados = DadosSensor.query.order_by(DadosSensor.timestamp.asc()).all()

    # Preparando os dados para os gráficos
    timestamps = [d.timestamp.strftime('%d/%m/%Y %H:%M:%S') for d in dados]
    temperaturas = [d.temperatura for d in dados]
    umidades = [d.umidade for d in dados]

    # Gráfico combinado de Temperatura e Umidade
    fig = go.Figure()

    # Linha de Temperatura
    fig.add_trace(go.Scatter(
        x=timestamps, 
        y=temperaturas, 
        mode='lines+markers', 
        name='Temperatura (°C)', 
        line=dict(color='#FF6347'),
        marker=dict(size=6),
        hovertemplate='Data: %{x}<br>Temperatura: %{y}°C<extra></extra>'
    ))

    # Linha de Umidade
    fig.add_trace(go.Scatter(
        x=timestamps, 
        y=umidades, 
        mode='lines+markers', 
        name='Umidade (%)', 
        line=dict(color='#4682B4'),
        marker=dict(size=6),
        hovertemplate='Data: %{x}<br>Umidade: %{y}%<extra></extra>'
    ))

    # Layout do gráfico
    fig.update_layout(
        title_text='Temperatura e Umidade ao Longo do Tempo',
        xaxis_title='Data e Hora',
        yaxis_title='Medições',
        legend=dict(
            x=1,  
            y=0.5,  
            font=dict(size=10),
            bgcolor="rgba(255, 255, 255, 0.5)"
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=False,
            tickangle=-45,  
            zeroline=False,
            nticks=10  
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=30, r=100, t=30, b=30),  
        hovermode="x"
    )

    # Converter o gráfico para HTML
    combined_graph = pio.to_html(fig, full_html=False)

    # Renderizar o template com o gráfico
    return render_template('dashboard.html', combined_graph=combined_graph)

# Rota para receber dados do ESP32
@app.route('/api/enviar_dados', methods=['POST'])
def receber_dados():
    dados = request.json
    temperatura = dados.get('temperatura')
    umidade = dados.get('umidade')

    if temperatura is None or umidade is None:
        return jsonify({"status": "erro", "mensagem": "Dados de temperatura ou umidade ausentes"}), 400

    novo_dado = DadosSensor(temperatura=temperatura, umidade=umidade)
    db.session.add(novo_dado)
    db.session.commit()

    return jsonify({"status": "sucesso", "dados_recebidos": dados}), 200

# Iniciar
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)