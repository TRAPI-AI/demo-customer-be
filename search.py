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
    data = request.get_json(force=True)
    api_key = os.getenv('DUFFEL_API_KEY')
    url = "https://api.duffel.com/air/offer_requests"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v2",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(url, headers=headers, json=data)
    return (jsonify(response.json()), response.status_code) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
