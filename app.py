from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS
#初始化 Flask-Login 扩展
from flask_login import LoginManager

db = SQLAlchemy()
# 初始化 LoginManager
login_manager = LoginManager()
# migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)

    from api import api_bp
    app.register_blueprint(api_bp)
    
    return app  