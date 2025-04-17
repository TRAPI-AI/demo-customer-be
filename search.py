from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
import time

app = Flask(__name__)
CORS(app)

load_dotenv()

DUFFEL_API_KEY = os.getenv('DUFFEL_API_KEY')
DUFFEL_URL = 'https://api.duffel.com/air/offer_requests'
HEADERS = {
    "Accept-Encoding": "gzip",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Duffel-Version": "v2",
    "Authorization": f"Bearer {DUFFEL_API_KEY}"
}
TIMEOUT = 60
MAX_RETRIES = 3

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the backend!"})

@app.route('/duffel-flights-list-offers', methods=['POST'])
def duffel_flights_list_offers():
    try:
        req_body = request.get_json(force=True)
        print(f"Request body: {json.dumps(req_body)}")
    except Exception as e:
        return jsonify({"error": "Invalid JSON in request body", "details": str(e)}), 400
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            resp = requests.post(
                DUFFEL_URL,
                headers=HEADERS,
                json=req_body,
                timeout=TIMEOUT
            )
            print(f"Duffel response status: {resp.status_code}")
            print(f"Duffel response body: {resp.text}")
            if resp.status_code >= 200 and resp.status_code < 300:
                return Response(resp.content, status=resp.status_code, content_type='application/json')
            else:
                if attempt == MAX_RETRIES - 1:
                    return jsonify({"error": "Duffel API error", "status_code": resp.status_code, "body": resp.text}), resp.status_code
        except requests.exceptions.Timeout:
            if attempt == MAX_RETRIES - 1:
                return jsonify({"error": "Duffel API request timed out"}), 504
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                return jsonify({"error": "Duffel API request failed", "details": str(e)}), 502
        attempt += 1
        time.sleep(2 ** attempt)
    return jsonify({"error": "Unknown error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
