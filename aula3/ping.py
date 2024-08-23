# Bibliotecas
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

# "Escapar" o nome e a senha
usuario = quote_plus("seuusuario")
senha = quote_plus("suasenha")

# URL
url = f"mongodb+srv://{usuario}:{senha}@cluster1.tjqkv.mongodb.net/?retryWrites=true&w=majority&appName=cluster1"

# Criar um novo cliente e conectar ao servidor
client = MongoClient(url, server_api = ServerApi('1'))

# Enviar a solicitação e confirmar a conexão
try:
    client.admin.command('ping')
    print("Sucesso ao conectar!")
except Exception as e:
    print(e)