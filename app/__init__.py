from flask import Flask
from flask_bootstrap import Bootstrap

from .config import Config

def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    app.config.from_object(Config)
    app.config['WTF_CSRF_ENABLED']= False

    return app
