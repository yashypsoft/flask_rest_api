# app/__init__.py

from flask import Flask
from .config import Config
from .db import init_db
from prometheus_flask_exporter import PrometheusMetrics

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize the database
    init_db(app)
    
    # Initialize Prometheus metrics
    metrics = PrometheusMetrics(app)
    
    # Import routes
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
