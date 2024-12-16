from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
import time

# Initializing Flask app
app = Flask(__name__)
CORS(app)

load_dotenv()

# Define your routes and logic here
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the backend!"})

# New route for Duffel flights list offers
@app.route('/duffel-flights-list-offers', methods=['POST'])
def duffel_flights_list_offers():
    duffel_api_key = os.getenv('DUFFEL_API_KEY')
    if not duffel_api_key:
        return jsonify({"error": "Duffel API key not found"}), 500

    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v2",
        "Authorization": f"Bearer {duffel_api_key}"
    }

    try:
        data = request.get_json()
        response = requests.post('https://api.duffel.com/air/offer_requests', headers=headers, json=data)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Ensure CORS is allowed if not already set
if not app.config.get('CORS_HEADERS'):
    CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure the app runs on port 5000 if not specified
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)))