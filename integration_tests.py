import unittest
import json
from flask import Flask
from flask.testing import FlaskClient
from search import app

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_home_endpoint(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Welcome to the backend!"})

    def test_hotel_availability_success(self):
        # Mock data for a successful request
        mock_data = {
            "stay": {
                "checkIn": "2023-12-20",
                "checkOut": "2023-12-25"
            },
            "occupancies": [
                {
                    "rooms": 1,
                    "adults": 2,
                    "children": 0
                }
            ],
            "destination": {
                "code": "PMI"
            }
        }
        response = self.client.post('/hotelbeds-hotels-booking-hotel-availability',
                                    data=json.dumps(mock_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)

    def test_hotel_availability_failure(self):
        # Mock data for a failed request
        mock_data = {
            "stay": {
                "checkIn": "2023-12-20",
                "checkOut": "2023-12-25"
            },
            "occupancies": [
                {
                    "rooms": 1,
                    "adults": 2,
                    "children": 0
                }
            ]
            # Missing destination code
        }
        response = self.client.post('/hotelbeds-hotels-booking-hotel-availability',
                                    data=json.dumps(mock_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertIn('application/json', response.content_type)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()