"""
Plik konfiguracyjny aplikacji.

Zawiera ustawienia dla różnych trybów działania aplikacji:
- Tryb deweloperski (do pracy nad projektem) - z debugowaniem włączonym
- Tryb produkcyjny (dla finalnej wersji) - z debugowaniem wyłączonym
"""

class Config:
    """Podstawowa konfiguracja - wspólne ustawienia dla wszystkich trybów."""
    DEBUG = True        # Czy włączyć tryb debugowania (pokazywanie szczegółów błędów)
    TESTING = False     # Czy aplikacja jest w trybie testowania

class ProductionConfig(Config):
    """Konfiguracja dla wersji produkcyjnej (użytkowej) aplikacji."""
    DEBUG = False       # W wersji produkcyjnej wyłączamy debugowanie dla bezpieczeństwa

class DevelopmentConfig(Config):
    """Konfiguracja dla trybu deweloperskiego (podczas tworzenia aplikacji)."""
    DEBUG = True        # Włączamy debugowanie, aby łatwiej znajdować błędy
