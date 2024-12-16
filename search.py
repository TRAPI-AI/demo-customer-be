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
    url = 'https://api.duffel.com/air/offer_requests'
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v2",
        "Authorization": f"Bearer {os.getenv('DUFFEL_API_KEY')}"
    }
    data = request.get_json()
    response = requests.post(url, headers=headers, json=data)
    return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])

if __name__ == '__main__':
    app.run(port=5000)