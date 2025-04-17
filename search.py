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

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the backend!"})

@app.route('/duffel-flights-list-offers', methods=['POST'])
def duffel_flights_list_offers():
    try:
        data = request.get_json()
        headers = {
            "Accept-Encoding": "gzip",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Duffel-Version": "v2",
            "Authorization": f"Bearer {os.getenv('DUFFEL_API_KEY')}"
        }
        url = "https://api.duffel.com/air/offer_requests"
        retries = 3
        timeout = 60
        for _ in range(retries):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=timeout)
                print("Request Body:", json.dumps(data, indent=2))
                print("Response Body:", response.text)
                response.raise_for_status()
                return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
            except requests.exceptions.RequestException as e:
                print("Error:", e)
                time.sleep(1)
        return jsonify({"error": "Failed to fetch offers after retries."}), 500
    except Exception as e:
        print("Unexpected Error:", e)
        return jsonify({"error": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
