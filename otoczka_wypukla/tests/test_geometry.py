import unittest
import sys
import os

# Add the parent directory to sys.path to allow importing 'core'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.geometry import cross_product, get_convex_hull, classify_shape

class TestGeometry(unittest.TestCase):
    
    def test_cross_product(self):
        # O=(0,0), A=(1,1), B=(0,1) -> Left turn (positive)
        self.assertGreater(cross_product((0,0), (1,1), (0,1)), 0)
        # O=(0,0), A=(1,1), B=(1,0) -> Right turn (negative)
        self.assertLess(cross_product((0,0), (1,1), (1,0)), 0)
        # O=(0,0), A=(1,1), B=(2,2) -> Collinear (zero)
        self.assertEqual(cross_product((0,0), (1,1), (2,2)), 0)

    def test_get_convex_hull_triangle(self):
        points = [[0, 0], [10, 0], [0, 10]]
        hull = get_convex_hull(points)
        self.assertEqual(len(hull), 3)
        # Check if points are in the hull (order might vary but sets should match)
        hull_set = set(tuple(p) for p in hull)
        points_set = set(tuple(p) for p in points)
        self.assertEqual(hull_set, points_set)

    def test_get_convex_hull_square(self):
        points = [[0, 0], [10, 0], [10, 10], [0, 10]]
        hull = get_convex_hull(points)
        self.assertEqual(len(hull), 4)

    def test_get_convex_hull_point_inside(self):
        # (2,2) is inside the triangle (0,0)-(10,0)-(0,10)
        points = [[0, 0], [10, 0], [0, 10], [2, 2]]
        hull = get_convex_hull(points)
        self.assertEqual(len(hull), 3)
        self.assertNotIn([2, 2], hull)

    def test_get_convex_hull_collinear(self):
        points = [[0, 0], [5, 5], [10, 10]]
        hull = get_convex_hull(points)
        # Should return endpoints [0,0] and [10,10]
        self.assertEqual(len(hull), 2)
        expected = {(0, 0), (10, 10)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_duplicates(self):
        points = [[0, 0], [0, 0], [10, 10]]
        hull = get_convex_hull(points)
        self.assertEqual(len(hull), 2)

    def test_get_convex_hull_collinear_4_points(self):
        """Test with 4 collinear points. Should return 2 endpoints."""
        points = [[0, 0], [1, 1], [2, 2], [3, 3]]
        hull = get_convex_hull(points)
        self.assertEqual(len(hull), 2)
        expected = {(0, 0), (3, 3)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_horizontal_line(self):
        """Test points on a horizontal line."""
        points = [[0, 5], [2, 5], [5, 5], [10, 5]]
        hull = get_convex_hull(points)
        self.assertEqual(len(hull), 2)
        expected = {(0, 5), (10, 5)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_vertical_line(self):
        """Test points on a vertical line."""
        points = [[5, 0], [5, 2], [5, 5], [5, 10]]
        hull = get_convex_hull(points)
        self.assertEqual(len(hull), 2)
        expected = {(5, 0), (5, 10)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_diamond_shape(self):
        """Test a diamond shape (rotated square)."""
        # (0, 10), (10, 0), (20, 10), (10, 20) -> All should be in hull
        points = [[0, 10], [10, 0], [20, 10], [10, 20], [10, 10]] # Center point included
        hull = get_convex_hull(points)
        self.assertEqual(len(hull), 4)
        expected = {(0, 10), (10, 0), (20, 10), (10, 20)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_negative_coordinates(self):
        """Test with negative coordinates to ensure algorithm generality."""
        points = [[-10, -10], [-5, -5], [0, 0], [-10, 0], [0, -10]]
        hull = get_convex_hull(points)
        # Should be a square/rectangle defined by corners (-10,-10), (-10,0), (0,0), (0,-10)
        # (-5, -5) is inside
        self.assertEqual(len(hull), 4)
        expected = {(-10, -10), (-10, 0), (0, 0), (0, -10)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_float_precision(self):
        """Test with floating point coordinates."""
        points = [[0.1, 0.1], [0.9, 0.1], [0.5, 0.8], [0.5, 0.4]]
        hull = get_convex_hull(points)
        # Triangle: (0.1, 0.1), (0.9, 0.1), (0.5, 0.8)
        # (0.5, 0.4) is inside
        self.assertEqual(len(hull), 3)
        expected = {(0.1, 0.1), (0.9, 0.1), (0.5, 0.8)}
        self.assertEqual(set(tuple(p) for p in hull), expected)

    def test_get_convex_hull_all_identical(self):
        """Test when all 4 points are the same."""
        points = [[5, 5], [5, 5], [5, 5], [5, 5]]
        hull = get_convex_hull(points)
        self.assertEqual(len(hull), 1)
        self.assertEqual(hull[0], [5, 5])

    def test_classify_shape(self):
        self.assertEqual(classify_shape([])[0], "Pusty")
        self.assertEqual(classify_shape([[0,0]])[0], "Punkt")
        self.assertEqual(classify_shape([[0,0], [1,1]])[0], "Odcinek")
        self.assertEqual(classify_shape([[0,0], [10,0], [0,10]])[0], "Trójkąt")
        self.assertEqual(classify_shape([[0,0], [10,0], [10,10], [0,10]])[0], "Czworokąt")
        
        poly_hull = [[0,0], [10,0], [10,10], [5, 12], [0,10]]
        name, desc = classify_shape(poly_hull)
        self.assertEqual(name, "Wielokąt (5)")

if __name__ == '__main__':
    unittest.main()
