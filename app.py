from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS


db = SQLAlchemy()
# migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
    app.config.from_object(config[config_name])
    
    db.init_app(app)

    from api import api_bp
    app.register_blueprint(api_bp)
    
    return app  