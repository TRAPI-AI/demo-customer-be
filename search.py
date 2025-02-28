from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
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
    payload = request.get_json()
    url = "https://api.duffel.com/air/offer_requests"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v2",
        "Authorization": f"Bearer {os.environ.get('DUFFEL_API_KEY')}"
    }
    r = requests.post(url, headers=headers, json=payload)
    return jsonify(r.json()), r.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
