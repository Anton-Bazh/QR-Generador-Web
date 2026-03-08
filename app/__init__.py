import os
from flask import Flask
from .utils.db import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_12345')
    
    # Init database
    init_db(app)

    # Register blueprints
    from .routes.main import main_bp
    from .routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    return app
