from flask import Flask
from flask_wtf.csrf import CSRFProtect

from config import Config

csrf = CSRFProtect()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)

    from .signatures import signatures_bp

    app.register_blueprint(signatures_bp)

    return app
