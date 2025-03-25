import requests
import os
import unittest
from unittest.mock import patch

class TestDuffelFlightsAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"

    @patch.dict(os.environ, {"DUFFEL_API_KEY": "test_api_key"})
    def test_duffel_flights_list_offers_success(self):
        # Mock request payload
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
                ]
            }
        }

        # Mock response from Duffel API
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "data": [
                    {
                        "id": "offer_123",
                        "total_amount": "500.00",
                        "total_currency": "USD"
                    }
                ]
            }

            response = requests.post(f"{self.BASE_URL}/duffel-flights-list-offers", json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertIn("data", response.json())
            self.assertEqual(response.json()["data"][0]["id"], "offer_123")

    @patch.dict(os.environ, {"DUFFEL_API_KEY": "test_api_key"})
    def test_duffel_flights_list_offers_failure(self):
        # Mock request payload
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
                ]
            }
        }

        # Mock response from Duffel API
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 400
            mock_post.return_value.json.return_value = {
                "error": "Invalid request"
            }

            response = requests.post(f"{self.BASE_URL}/duffel-flights-list-offers", json=payload)
            self.assertEqual(response.status_code, 400)
            self.assertIn("error", response.json())
            self.assertEqual(response.json()["error"], "Invalid request")

if __name__ == "__main__":
    unittest.main()