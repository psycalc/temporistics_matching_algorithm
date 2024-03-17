import unittest
from app import create_app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Psychological Calculator', response.data)

    def test_change_language_route(self):
        response = self.client.post('/change_language', json={'language': 'en'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"success":true}', response.data)

    # Add more test cases for other routes and scenarios

if __name__ == '__main__':
    unittest.main()