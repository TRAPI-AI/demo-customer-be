# demo-customer-be
import xml.etree.ElementTree as ET
from lxml import etree
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

@app.route('/hotelbeds-hotels-booking-hotel-availability', methods=['POST'])
def hotelbeds_hotels_booking_hotel_availability():
    try:
        api_key = os.getenv('HOTELBEDS_HOTEL_API_KEY')
        secret = os.getenv('HOTELBEDS_HOTEL_SECRET')
        timestamp = str(int(time.time()))
        signature = hashlib.sha256((api_key + secret + timestamp).encode('utf-8')).hexdigest()

        headers = {
            'Accept': 'application/json',
            'Api-key': api_key,
            'X-Signature': signature,
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json'
        }

        response = requests.post('https://api.test.hotelbeds.com/hotel-api/v1/hotels', headers=headers, json=request.json)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return jsonify({"error": str(e)}), 500

# Running the app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
