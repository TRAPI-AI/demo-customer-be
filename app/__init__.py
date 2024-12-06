"""__init__.py"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from . import routes


def create_app():
    """Create App"""
    app = Flask(__name__)
    CORS(app)
    load_dotenv()

    with app.app_context():
        app.register_blueprint(routes.router)

    return app
