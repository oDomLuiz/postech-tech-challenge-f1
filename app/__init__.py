from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import api_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'your-secret-key'
    db.init_app(app)

    app.register_blueprint(api_bp)

    return app
