# Bibliotecas
from routes.auth import bp as auth_bp
from routes.main import bp as main_bp

# Registrar as blueprints
def registrar_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)