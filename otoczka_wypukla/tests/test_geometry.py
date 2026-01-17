"""
Testy jednostkowe dla funkcji geometrycznych.

Ten plik zawiera automatyczne testy sprawdzające, czy funkcje obliczające
otoczkę wypukłą działają poprawnie w różnych sytuacjach.
"""

import unittest
import sys
import os

# Dodajemy katalog nadrzędny do ścieżki, aby móc zaimportować moduł 'core'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.geometry import cross_product, get_convex_hull, classify_shape

class TestGeometry(unittest.TestCase):
    """Klasa zawierająca testy funkcji geometrycznych."""
    
    def test_cross_product(self):
        """Test funkcji określającej kierunek skrętu między trzema punktami."""
        # O=(0,0), A=(1,1), B=(0,1) -> Skręt w lewo (wynik dodatni)
        self.assertGreater(cross_product((0,0), (1,1), (0,1)), 0)
        
        # O=(0,0), A=(1,1), B=(1,0) -> Skręt w prawo (wynik ujemny)
        self.assertLess(cross_product((0,0), (1,1), (1,0)), 0)
        
        # O=(0,0), A=(1,1), B=(2,2) -> Punkty na jednej prostej (wynik zero)
        self.assertEqual(cross_product((0,0), (1,1), (2,2)), 0)

    def test_get_convex_hull_triangle(self):
        """Test dla trzech punktów tworzących trójkąt."""
        points = [[0, 0], [10, 0], [0, 10]]
        hull = get_convex_hull(points)
        # Otoczka powinna mieć 3 wierzchołki
        self.assertEqual(len(hull), 3)
        # Sprawdzamy, czy wszystkie punkty są w otoczce (kolejność może się różnić)
        hull_set = set(tuple(p) for p in hull)
        points_set = set(tuple(p) for p in points)
        self.assertEqual(hull_set, points_set)

    def test_get_convex_hull_square(self):
        """Test dla czterech punktów tworzących kwadrat."""
        points = [[0, 0], [10, 0], [10, 10], [0, 10]]
        hull = get_convex_hull(points)
        # Wszystkie 4 punkty powinny być w otoczce
        self.assertEqual(len(hull), 4)

    def test_get_convex_hull_point_inside(self):
        """Test gdy jeden punkt leży wewnątrz trójkąta utworzonego przez pozostałe."""
        # Punkt (2,2) znajduje się wewnątrz trójkąta (0,0)-(10,0)-(0,10)
        points = [[0, 0], [10, 0], [0, 10], [2, 2]]
        hull = get_convex_hull(points)
        # Otoczka powinna mieć tylko 3 wierzchołki (bez punktu środkowego)
        self.assertEqual(len(hull), 3)
        self.assertNotIn([2, 2], hull)

    def test_get_convex_hull_collinear(self):
        """Test dla punktów leżących na jednej linii prostej (współliniowych)."""
        points = [[0, 0], [5, 5], [10, 10]]
        hull = get_convex_hull(points)
        # Powinniśmy otrzymać tylko 2 punkty skrajne: [0,0] i [10,10]
        self.assertEqual(len(hull), 2)
        expected = {(0, 0), (10, 10)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_duplicates(self):
        """Test dla punktów powtarzających się (duplikatów)."""
        points = [[0, 0], [0, 0], [10, 10]]
        hull = get_convex_hull(points)
        # Duplikaty powinny być usunięte, zostają 2 punkty
        self.assertEqual(len(hull), 2)

    def test_get_convex_hull_collinear_4_points(self):
        """Test dla 4 punktów leżących na jednej linii prostej."""
        points = [[0, 0], [1, 1], [2, 2], [3, 3]]
        hull = get_convex_hull(points)
        # Powinniśmy otrzymać tylko 2 punkty skrajne
        self.assertEqual(len(hull), 2)
        expected = {(0, 0), (3, 3)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_horizontal_line(self):
        """Test dla punktów ułożonych wzdłuż poziomej linii."""
        points = [[0, 5], [2, 5], [5, 5], [10, 5]]
        hull = get_convex_hull(points)
        # Tylko punkty skrajne: lewy i prawy
        self.assertEqual(len(hull), 2)
        expected = {(0, 5), (10, 5)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_vertical_line(self):
        """Test dla punktów ułożonych wzdłuż pionowej linii."""
        points = [[5, 0], [5, 2], [5, 5], [5, 10]]
        hull = get_convex_hull(points)
        # Tylko punkty skrajne: dolny i górny
        self.assertEqual(len(hull), 2)
        expected = {(5, 0), (5, 10)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_diamond_shape(self):
        """Test dla punktów tworzących romb (obrócony kwadrat)."""
        # 4 narożniki rombu + punkt środkowy
        points = [[0, 10], [10, 0], [20, 10], [10, 20], [10, 10]]
        hull = get_convex_hull(points)
        # Punkt środkowy nie powinien być w otoczce - zostają 4 narożniki
        self.assertEqual(len(hull), 4)
        expected = {(0, 10), (10, 0), (20, 10), (10, 20)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_negative_coordinates(self):
        """Test ze współrzędnymi ujemnymi - sprawdza ogólność algorytmu."""
        points = [[-10, -10], [-5, -5], [0, 0], [-10, 0], [0, -10]]
        hull = get_convex_hull(points)
        # Kwadrat/prostokąt z narożnikami (-10,-10), (-10,0), (0,0), (0,-10)
        # Punkt (-5, -5) leży w środku
        self.assertEqual(len(hull), 4)
        expected = {(-10, -10), (-10, 0), (0, 0), (0, -10)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_float_precision(self):
        """Test ze współrzędnymi zmiennoprzecinkowymi (z częścią dziesiętną)."""
        points = [[0.1, 0.1], [0.9, 0.1], [0.5, 0.8], [0.5, 0.4]]
        hull = get_convex_hull(points)
        # Trójkąt: (0.1, 0.1), (0.9, 0.1), (0.5, 0.8)
        # Punkt (0.5, 0.4) leży wewnątrz
        self.assertEqual(len(hull), 3)
        expected = {(0.1, 0.1), (0.9, 0.1), (0.5, 0.8)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_all_identical(self):
        """Test gdy wszystkie 4 punkty są identyczne (w tym samym miejscu)."""
        points = [[5, 5], [5, 5], [5, 5], [5, 5]]
        hull = get_convex_hull(points)
        # Powinien zostać tylko jeden punkt
        self.assertEqual(len(hull), 1)
        self.assertEqual(hull[0], [5, 5])

    def test_classify_shape(self):
        """Test funkcji klasyfikującej kształt otoczki."""
        # Pusta otoczka
        self.assertEqual(classify_shape([])[0], "Pusty")
        
        # Pojedynczy punkt
        self.assertEqual(classify_shape([[0,0]])[0], "Punkt")
        
        # Odcinek (linia)
        self.assertEqual(classify_shape([[0,0], [1,1]])[0], "Odcinek")
        
        # Trójkąt
        self.assertEqual(classify_shape([[0,0], [10,0], [0,10]])[0], "Trójkąt")
        
        # Czworokąt
        self.assertEqual(classify_shape([[0,0], [10,0], [10,10], [0,10]])[0], "Czworokąt")
        
        # Wielokąt o 5 wierzchołkach
        poly_hull = [[0,0], [10,0], [10,10], [5, 12], [0,10]]
        name, desc = classify_shape(poly_hull)
        self.assertEqual(name, "Wielokąt (5)")

# Uruchomienie testów gdy plik jest wykonywany bezpośrednio
if __name__ == '__main__':
    unittest.main()
