from flask import Flask, redirect, url_for, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'cartoonimations.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Add a root route to the main app
    @app.route('/')
    def index():
        return jsonify({
            "status": "ok",
            "message": "Cartoonimations API is running",
            "endpoints": {
                "health": "/api/health",
                "generate": "/api/generate (POST)"
            }
        })

    # Register routes
    from .routes import main_routes
    app.register_blueprint(main_routes.bp)

    return app