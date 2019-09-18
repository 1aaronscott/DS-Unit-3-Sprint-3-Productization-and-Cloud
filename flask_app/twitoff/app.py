"""
Main application and routing logic for TwitOff.
"""

from flask import Flask
from .models import DB


def create_app():
    """create and config an instance of the flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def root():
        return "Welcome to TwitOff!"
    return app
