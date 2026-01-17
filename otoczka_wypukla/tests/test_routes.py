import unittest
import sys
import os
import json

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web import create_app

class TestRoutes(unittest.TestCase):
    
    def setUp(self):
        # Use a testing config if available, otherwise default
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check if basic HTML structure or title is present (rudimentary check)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_calculate_valid(self):
        payload = {
            "points": [[0, 0], [10, 0], [0, 10], [2, 2]]
        }
        response = self.client.post('/calculate', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn('hull', data)
        self.assertIn('shape_type', data)
        self.assertIn('description', data)
        
        # Expecting a triangle (3 points in hull) as (2,2) is inside
        self.assertEqual(len(data['hull']), 3)
        self.assertEqual(data['shape_type'], 'Trójkąt')

    def test_calculate_empty(self):
        payload = {"points": []}
        response = self.client.post('/calculate', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_calculate_no_points_key(self):
        payload = {"other_key": []}
        response = self.client.post('/calculate', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        # Based on routes.py: points = data.get('points', []) -> returns empty list if missing
        # if not points: return 400
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
