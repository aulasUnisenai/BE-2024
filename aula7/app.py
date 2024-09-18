# Bibliotecas
from flask import Flask
from config import Config
from extensions import db, login_manager
from routes import registrar_blueprints
from models import Usuario