from flask import Flask, render_template
import socketio
from flask_cors import CORS
import random

# Cria uma instância do Flask
app = Flask(__name__, template_folder='templates')

# Habilita o CORS para o aplicativo Flask, permitindo solicitações de diferentes origens
CORS(app)

# Cria uma instância do Socket.IO com permissões para conexões de qualquer origem
sio = socketio.Server(cors_allowed_origins="*")
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Dicionário para armazenar as cores associadas a cada usuário
user_colors = {}

def get_random_color():
    # Retorna uma cor hexadecimal aleatória
    return f'#{random.randint(0, 0xFFFFFF):06x}'

@app.route('/')
def index():
    # Renderiza o template HTML para a página inicial
    return render_template('index.html')

@sio.event
def connect(sid, environ):
    # Evento acionado quando um cliente se conecta
    print(f'Novo cliente conectado: {sid}')
    # Atribui uma cor ao novo usuário
    user_colors[sid] = get_random_color()

@sio.event
def message(sid, data):
    # Evento acionado quando uma mensagem é recebida de um cliente
    print(f'Mensagem recebida de {sid}: {data}')
    # Obtém a cor associada ao usuário, ou usa preto como padrão
    color = user_colors.get(sid, '#000000')
    # Emite a mensagem para todos os clientes conectados, incluindo a cor do remetente
    sio.emit('message', {'data': data, 'color': color})

@sio.event
def disconnect(sid):
    # Evento acionado quando um cliente se desconecta
    print(f'Cliente desconectado: {sid}')
    # Remove o usuário desconectado do dicionário de cores
    if sid in user_colors:
        del user_colors[sid]

if __name__ == '__main__':
    import eventlet
    # Executa o servidor WSGI com Eventlet na porta 5000
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)