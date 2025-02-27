from flask import Flask, request, jsonify
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
    data = request.get_json()
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v2",
        "Authorization": f"Bearer {os.getenv('DUFFEL_API_KEY')}"
    }
    resp = requests.post("https://api.duffel.com/air/offer_requests", json=data, headers=headers)
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
