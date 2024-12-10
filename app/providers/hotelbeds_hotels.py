import os
import time
import hashlib
from flask import request, jsonify, Response
import requests


def generate_signature(api_key, secret, timestamp):
    """Generate a signature for Hotelbeds API authentication."""
    return hashlib.sha256((api_key + secret + timestamp).encode("utf-8")).hexdigest()


def transform_to_hotelbeds_request(frontend_data):
    """Transform frontend request data to Hotelbeds API request format."""
    return {
        "stay": {
            "checkIn": frontend_data["stay"]["checkIn"],
            "checkOut": frontend_data["stay"]["checkOut"],
        },
        "occupancies": frontend_data["occupancies"],
        "geolocation": frontend_data["geolocation"],
    }


def get_hotel_availability():
    """Fetch hotel availability from Hotelbeds API."""
    print("Calling Hotelbeds")
    try:
        # Transform the incoming request data
        frontend_data = request.json
        hotelbeds_request = transform_to_hotelbeds_request(frontend_data)

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
            json=hotelbeds_request,
            timeout=10,
        )
        print(f"Hotelbeds response status: {response.status_code}")
        print(
            f"Hotelbeds response content (truncated): {str(response.content)[:200]}..."
        )
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers["Content-Type"],
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
