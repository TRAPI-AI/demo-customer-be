import requests
import time
import logging

class NewProviderAdapter:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def fetch_data(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        retries = 3
        backoff_factor = 1

        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=60)
                response.raise_for_status()
                print("Request URL:", response.url)
                print("Request Headers:", response.request.headers)
                print("Response Status Code:", response.status_code)
                print("Response JSON:", response.json())
                return response.json()
            except requests.exceptions.Timeout:
                logging.warning(f"Timeout occurred for {url}. Retrying {attempt + 1}/{retries}...")
            except requests.exceptions.ConnectionError as e:
                logging.error(f"Connection error: {e}. Retrying {attempt + 1}/{retries}...")
            except requests.exceptions.HTTPError as e:
                if 500 <= response.status_code < 600:
                    logging.error(f"Server error: {e}. Retrying {attempt + 1}/{retries}...")
                else:
                    logging.error(f"HTTP error: {e}. No retry.")
                    break
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
                break
            time.sleep(backoff_factor * (2 ** attempt))
        return None

# Example usage
# adapter = NewProviderAdapter(base_url='https://api.example.com', headers={'Authorization': 'Bearer token'})
# data = adapter.fetch_data('some/endpoint')