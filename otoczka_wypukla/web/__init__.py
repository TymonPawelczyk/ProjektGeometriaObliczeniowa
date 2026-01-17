from flask import Flask

def create_app(config_object='config.DevelopmentConfig'):
    app = Flask(__name__)
    
    # Ładowanie konfiguracji
    try:
        app.config.from_object(config_object)
    except ImportError:
        pass # Fallback do domyślnych

    # Rejestracja Blueprintów
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)
        
    return app