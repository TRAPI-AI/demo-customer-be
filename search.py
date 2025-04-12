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

@app.route('/hotelbeds-hotels-booking-hotel-availability', methods=['POST'])
def hotel_availability():
    try:
        data = request.get_json()
        print("Request Body:", data)
        api_key = os.getenv('HOTELBEDS_HOTEL_API_KEY')
        secret = os.getenv('HOTELBEDS_HOTEL_SECRET')
        timestamp = str(int(time.time()))
        signature = hashlib.sha256((api_key + secret + timestamp).encode('utf-8')).hexdigest()
        headers = {
            'Accept': 'application/json',
            'Api-key': api_key,
            'X-Signature': signature,
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip'
        }
        url = 'https://api.test.hotelbeds.com/hotel-api/v1/hotels'
        for _ in range(3):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=60)
                print("Response Body:", response.json())
                return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
            except requests.exceptions.RequestException as e:
                print("Request failed:", e)
        return jsonify({"error": "Failed to fetch hotel availability after retries."}), 503
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred processing your request."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)