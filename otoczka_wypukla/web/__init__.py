from flask import Flask

def create_app(config_object='config.DevelopmentConfig'):
    """
    Tworzy i konfiguruje aplikację Flask.
    
    Ta funkcja jest "fabryką aplikacji" - przygotowuje całą aplikację webową,
    ładuje ustawienia i rejestruje wszystkie potrzebne komponenty (blueprinty).
    
    Parametry:
        config_object: Nazwa klasy z ustawieniami (domyślnie: konfiguracja deweloperska)
    
    Zwraca:
        Gotową do uruchomienia aplikację Flask
    """
    # Tworzymy nową aplikację Flask
    app = Flask(__name__)
    
    # Ładujemy konfigurację (ustawienia aplikacji jak tryb debugowania, itp.)
    try:
        app.config.from_object(config_object)
    except ImportError:
        # Jeśli nie uda się załadować konfiguracji, używamy domyślnych ustawień
        pass

    # Rejestrujemy Blueprint (moduł) odpowiedzialny za obsługę stron i obliczeń
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)
        
    return app