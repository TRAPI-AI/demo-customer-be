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

    data = request.get_json()
    url = 'https://api.test.hotelbeds.com/hotel-api/v1/hotels'

    response = requests.post(url, headers=headers, json=data)

    return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])