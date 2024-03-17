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
        response = self.client.post('/change_language', data={'language': 'en'})
        self.assertEqual(response.status_code, 302)

    def test_get_types_route_temporistics(self):
        response = self.client.get('/get_types?typology=Temporistics')
        self.assertEqual(response.status_code, 200)
        # Assert based on expected types data, e.g., 
        # self.assertIn(b'"types":', response.data)

    def test_get_types_route_psychosophia(self):
        response = self.client.get('/get_types?typology=Psychosophia')
        self.assertEqual(response.status_code, 200)
        # Assert based on expected types data

    def test_get_types_route_amatoric(self):
        response = self.client.get('/get_types?typology=Amatoric')
        self.assertEqual(response.status_code, 200)
        # Assert based on expected types data

    def test_get_types_route_socionics(self):
        response = self.client.get('/get_types?typology=Socionics')
        self.assertEqual(response.status_code, 200)
        # Assert based on expected types data

    # Add tests for any other routes, for example, a route that handles form submission:
    def test_relationship_calculation(self):
        # Replace 'user1_type', 'user2_type', and 'typology' with your actual form field names and test data
        form_data = {'user1': 'Type1', 'user2': 'Type2', 'typology': 'Temporistics'}
        response = self.client.post('/', data=form_data)
        self.assertEqual(response.status_code, 200)
        # Assert based on expected response, e.g., 
        # self.assertIn(b'Relationship Type:', response.data)

    # Add more test cases for other routes and scenarios

if __name__ == '__main__':
    unittest.main()
