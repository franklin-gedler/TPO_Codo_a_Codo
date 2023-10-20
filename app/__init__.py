from flask import Flask
from .backend.back_routes import backend_bp
from .frontend.front_routes import frontend_bp
from .health.views import health
from app.config import Config

app = Flask(__name__, template_folder="frontend/templates")
app.config.from_object(Config)

# Configura la carpeta de archivos estáticos
app.static_folder = "frontend/static"
#app.config['STATIC_URL'] = '/static/'

# routes
app.register_blueprint(frontend_bp)
app.register_blueprint(backend_bp)
app.register_blueprint(health)
