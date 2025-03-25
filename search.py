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
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v2",
        "Authorization": f"Bearer {os.getenv('DUFFEL_API_KEY')}"
    }
    response = requests.post('https://api.duffel.com/air/offer_requests', headers=headers, json=request.json)
    return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
