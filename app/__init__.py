from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # App Config
    app.config['SECRET_KEY'] = "secret-key"

    # Add Database
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

    db.init_app(app)

    # Flask Login 
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .routes import main
    app.register_blueprint(main)

    return app

