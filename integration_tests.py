import unittest
import requests
import os
from dotenv import load_dotenv

class TestDuffelFlightsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.base_url = "http://localhost:5000"
        cls.duffel_api_key = os.getenv('DUFFEL_API_KEY')
        if not cls.duffel_api_key:
            raise ValueError("DUFFEL_API_KEY not set in environment variables")

    def test_home_endpoint(self):
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Welcome to the backend!", response.json().get("message", ""))

    def test_duffel_flights_list_offers(self):
        url = f"{self.base_url}/duffel-flights-list-offers"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "data": {
                "slices": [
                    {
                        "origin": "LHR",
                        "destination": "JFK",
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
        }
        response = requests.post(url, headers=headers, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())

if __name__ == '__main__':
    unittest.main()