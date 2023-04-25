""" main module """

from flask import Flask
from .blueprints.folder import folder as folder_blueprint


def create_app(config_file: str = "config_flask_app.py") -> Flask:
    """
    create app
    """
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.register_blueprint(folder_blueprint)

    return app