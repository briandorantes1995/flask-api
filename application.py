"""
application.py
- creates a Flask app instance and registers the database object
"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv, dotenv_values

load_dotenv()


def create_app(app_name='SURVEY_API'):
    app = Flask(app_name)
    config = dotenv_values()
    app.config.from_mapping(config)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    from api import api
    app.register_blueprint(api, url_prefix="/api")

    from models import db
    db.init_app(app)

    return app
