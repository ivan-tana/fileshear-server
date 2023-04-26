""" main module """

from flask import Flask
from src.app.folder import folder as folder_blueprint
from .extensions import database
from src.app.models.Folder import Folder


def create_app(config_file: str = "config_flask_app.py") -> Flask:
    """
    create app
    """
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.register_blueprint(folder_blueprint)
    database.init_app(app)
    with app.app_context():
        database.create_all()

    return app
