from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the backend!"})

@app.route('/duffel-flights-list-offers', methods=['POST'])
def duffel_flights_list_offers():
    try:
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

        data = request.json
        response = requests.post('https://api.duffel.com/air/offer_requests', headers=headers, json=data)

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch offers", "details": response.text}), response.status_code

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500