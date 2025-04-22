import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)
CORS(app)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

DUFFEL_API_KEY = os.getenv('DUFFEL_API_KEY', 'YOUR_DUFFEL_API_KEY')
DUFFEL_URL = 'https://api.duffel.com/air/offer_requests'
HEADERS = {
    'Accept-Encoding': 'gzip',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Duffel-Version': 'v2',
    'Authorization': f'Bearer {DUFFEL_API_KEY}'
}
TIMEOUT = 60
RETRIES = 3
BACKOFF_FACTOR = 1

session = requests.Session()
retries = Retry(total=RETRIES, backoff_factor=BACKOFF_FACTOR, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["POST"])
adapter = HTTPAdapter(max_retries=retries)
session.mount('https://', adapter)
session.mount('http://', adapter)

@app.route('/duffel-flights-list-offers', methods=['POST'])
def duffel_flights_list_offers():
    try:
        req_body = request.get_json(force=True)
        logging.info(f"Request body: {req_body}")
        resp = session.post(DUFFEL_URL, json=req_body, headers=HEADERS, timeout=TIMEOUT)
        logging.info(f"Duffel response: {resp.text}")
        resp.raise_for_status()
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.Timeout:
        logging.error("Duffel API request timed out.")
        return jsonify({'error': 'Duffel API request timed out.'}), 504
    except requests.exceptions.RequestException as e:
        logging.error(f"Duffel API request error: {str(e)}")
        return jsonify({'error': 'Duffel API request error', 'details': str(e)}), 502
    except Exception as e:
        logging.error(f"Internal server error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
