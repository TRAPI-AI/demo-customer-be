import unittest
import requests
import os
from dotenv import load_dotenv

class TestDuffelFlightsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.base_url = 'http://localhost:5000'
        cls.duffel_api_key = os.getenv('DUFFEL_API_KEY')
        if not cls.duffel_api_key:
            raise Exception("Duffel API key not found in environment variables")

    def test_home_endpoint(self):
        response = requests.get(f'{self.base_url}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the backend!', response.json().get('message', ''))

    def test_duffel_flights_list_offers_valid_request(self):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            # Example data structure, replace with actual valid data
            "slices": [
                {
                    "origin": "JFK",
                    "destination": "LHR",
                    "departure_date": "2023-12-01"
                }
            ],
            "passengers": [
                {
                    "type": "adult"
                }
            ],
            "cabin_class": "economy"
        }
        response = requests.post(f'{self.base_url}/duffel-flights-list-offers', headers=headers, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())

    def test_duffel_flights_list_offers_invalid_request(self):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            # Invalid data structure
            "invalid_key": "invalid_value"
        }
        response = requests.post(f'{self.base_url}/duffel-flights-list-offers', headers=headers, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_duffel_flights_list_offers_missing_api_key(self):
        # Temporarily remove the API key from the environment
        original_api_key = os.environ.pop('DUFFEL_API_KEY', None)
        try:
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "slices": [
                    {
                        "origin": "JFK",
                        "destination": "LHR",
                        "departure_date": "2023-12-01"
                    }
                ],
                "passengers": [
                    {
                        "type": "adult"
                    }
                ],
                "cabin_class": "economy"
            }
            response = requests.post(f'{self.base_url}/duffel-flights-list-offers', headers=headers, json=data)
            self.assertEqual(response.status_code, 500)
            self.assertIn('Duffel API key not found', response.json().get('error', ''))
        finally:
            # Restore the API key
            if original_api_key:
                os.environ['DUFFEL_API_KEY'] = original_api_key

if __name__ == '__main__':
    unittest.main()