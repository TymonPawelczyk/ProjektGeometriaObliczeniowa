from flask import Blueprint, render_template, request, jsonify
from core.geometry import get_convex_hull, classify_shape

# Tworzymy Blueprint 'main' - moduł odpowiedzialny za obsługę stron i żądań użytkownika
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    Strona główna aplikacji.
    
    Ta funkcja wyświetla główną stronę z interaktywnym płótnem do zaznaczania punktów i obliczania otoczki wypukłej.
    """
    return render_template('index.html')

@bp.route('/calculate', methods=['POST'])
def calculate():
    """
    Oblicza otoczkę wypukłą dla podanych punktów.
    
    Ta funkcja przyjmuje punkty wysłane z przeglądarki (przez JavaScript), oblicza dla nich otoczkę wypukłą, rozpoznaje kształt i odsyła wyniki z powrotem do przeglądarki.
    
    Oczekiwane dane wejściowe (JSON):
        {
            "points": [[x1, y1], [x2, y2], ...]
        }
    
    Zwracane dane (JSON):
        {
            "hull": [[x1, y1], ...],        # Wierzchołki otoczki
            "shape_type": "Trójkąt",         # Nazwa kształtu
            "description": "Opis..."         # Wyjaśnienie wyniku
        }
    """
    # Pobieramy dane JSON wysłane z przeglądarki
    data = request.json
    points = data.get('points', [])
    
    # Sprawdzamy, czy użytkownik podał jakieś punkty
    if not points:
        return jsonify({'error': 'Brak punktów'}), 400

    # Obliczamy otoczkę wypukłą dla podanych punktów
    hull = get_convex_hull(points)
    
    # Rozpoznajemy, jaki kształt utworzył się z otoczki
    shape_type, description = classify_shape(hull)
    
    # Odsyłamy wyniki z powrotem do przeglądarki
    return jsonify({
        'hull': hull,
        'shape_type': shape_type,
        'description': description
    })