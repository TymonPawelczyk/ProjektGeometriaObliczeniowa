"""
Główny plik uruchamiający aplikację.

Ten skrypt uruchamia serwer webowy z aplikacją do obliczania otoczki wypukłej.
Po uruchomieniu, aplikacja będzie dostępna pod adresem: http://localhost:5000
"""

from web import create_app

# Tworzymy aplikację (ładujemy wszystkie potrzebne komponenty)
app = create_app()

# Uruchamiamy aplikację tylko jeśli ten plik został uruchomiony bezpośrednio
if __name__ == '__main__':
    print("Uruchamianie serwera Geometrii Obliczeniowej...")
    print("Otwórz przeglądarkę i wejdź na: http://localhost:5000")
    # Uruchamiamy serwer z trybem debugowania i na porcie 5000
    app.run(debug=True, port=5000)
