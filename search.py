from flask import Flask, request, jsonify, Response
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

def duffel_offers():
    payload = request.get_json()
    key = os.environ.get('DUFFEL_API_KEY')
    headers = {
        "Accept-Encoding": "gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": "v2",
        "Authorization": f"Bearer {key}"
    }
    r = requests.post("https://api.duffel.com/air/offer_requests", json=payload, headers=headers)
    return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type", "application/json"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
