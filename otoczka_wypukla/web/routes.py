from flask import Blueprint, render_template, request, jsonify
from core.geometry import get_convex_hull, classify_shape

# Tworzymy Blueprint 'main'
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    points = data.get('points', [])
    
    if not points:
        return jsonify({'error': 'Brak punktów'}), 400

    # Logika biznesowa
    hull = get_convex_hull(points)
    shape_type, description = classify_shape(hull)
    
    return jsonify({
        'hull': hull,
        'shape_type': shape_type,
        'description': description
    })