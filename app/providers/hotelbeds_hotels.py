"""hotelbeds_hotels.py"""

import os
import time
import hashlib
from flask import request, jsonify, Response
import requests


def generate_signature(api_key, secret, timestamp):
    """Generate a signature for Hotelbeds API authentication."""
    return hashlib.sha256((api_key + secret + timestamp).encode("utf-8")).hexdigest()


def get_hotel_availability():
    """Fetch hotel availability from Hotelbeds API."""
    try:
        data = request.json
        api_key = os.getenv("HOTELBEDS_HOTEL_API_KEY")
        secret = os.getenv("HOTELBEDS_HOTEL_SECRET")
        timestamp = str(int(time.time()))
        signature = generate_signature(api_key, secret, timestamp)

        headers = {
            "Accept": "application/json",
            "Api-key": api_key,
            "X-Signature": signature,
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip",
        }

        response = requests.post(
            "https://api.test.hotelbeds.com/hotel-api/v1/hotels",
            headers=headers,
            json=data,
            timeout=10,
        )
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers["Content-Type"],
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
