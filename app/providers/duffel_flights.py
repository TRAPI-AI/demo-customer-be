"""duffel_flights.py"""

import requests
from flask import jsonify

DUFFEL_API_URL = "https://api.duffel.com/air/offer_requests"
HEADERS = {
    "Accept-Encoding": "gzip",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Duffel-Version": "v2",
    "Authorization": "Bearer {{DUFFEL_API_KEY}}"
}

def list_duffel_flight_offers(data):
    response = requests.post(DUFFEL_API_URL, headers=HEADERS, json=data)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code