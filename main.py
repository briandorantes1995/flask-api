# app.py
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv, dotenv_values
from models import db
from api import api

load_dotenv()


app = Flask(__name__)
config = dotenv_values()
app.config.from_mapping(config)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(api, url_prefix="/api")
db.init_app(app)


if __name__ == '__main__':

    app.run(debug=True, port=8056)
