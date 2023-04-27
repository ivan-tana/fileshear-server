""" main module """

from flask import Flask
from .folder import folder as folder_blueprint
from .get_resources import get_resources as get_resources_blueprint
from .extensions import database

# blueprints
blueprints = [
    get_resources_blueprint,
    folder_blueprint
]


def create_app(config_file: str = "config_flask_app.py") -> Flask:
    """
    create app
    """
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    # register blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # initialize database
    database.init_app(app)

    with app.app_context():
        database.create_all()

    return app
