from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

DUFFEL_API_KEY = os.environ.get("DUFFEL_API_KEY")

@app.route("/duffel-flights-list-offers", methods=["POST"])
def duffel_flights_list_offers():
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v2",
        "Authorization": f"Bearer {DUFFEL_API_KEY}"
    }
    body = request.get_json()
    url = "https://api.duffel.com/air/offer_requests"
    response = requests.post(url, headers=headers, json=body)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(port=5000)
