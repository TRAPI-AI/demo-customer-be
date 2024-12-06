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

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the backend!"})

@app.route('/hotelbeds-hotels-booking-hotel-availability', methods=['POST'])
def hotel_availability():
    try:
        data = request.json
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

        response = requests.post('https://api.test.hotelbeds.com/hotel-api/v1/hotels', headers=headers, json=data)
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)