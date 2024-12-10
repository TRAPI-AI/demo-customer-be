"""hotelbeds_hotels.py"""

import os
import time
import hashlib
from flask import request, jsonify
import requests
from marshmallow import ValidationError
from app.schemas.hotelbeds.hotelbeds_search_schema import HotelBedsRequestSchema


def generate_signature(api_key, secret, timestamp):
    """Generate a signature for Hotelbeds API authentication."""
    return hashlib.sha256((api_key + secret + timestamp).encode("utf-8")).hexdigest()


def transform_to_hotelbeds_request(frontend_data):
    """Transform frontend request data to Hotelbeds API request format."""
    check_in = frontend_data["stay"]["checkIn"]
    check_out = frontend_data["stay"]["checkOut"]

    if hasattr(check_in, "strftime"):
        check_in = check_in.strftime("%Y-%m-%d")
    if hasattr(check_out, "strftime"):
        check_out = check_out.strftime("%Y-%m-%d")

    return {
        "stay": {
            "checkIn": check_in,
            "checkOut": check_out,
        },
        "occupancies": frontend_data["occupancies"],
        "geolocation": frontend_data["geolocation"],
    }


def normalize_hotelbeds_response(response_json):
    """Normalize Hotelbeds API response to a consistent format."""
    hotels = response_json.get("hotels", {}).get("hotels", [])
    normalized_hotels = []

    for hotel in hotels:
        normalized_hotel = {
            "code": hotel.get("code"),
            "destinationName": hotel.get("destinationName"),
            "zoneName": hotel.get("zoneName"),
            "discount": hotel.get("rooms", [{}])[0]
            .get("rates", [{}])[0]
            .get("discount"),
            "rateClass": hotel.get("rooms", [{}])[0]
            .get("rates", [{}])[0]
            .get("rateClass"),
            "categoryName": hotel.get("categoryName"),
            "boardName": hotel.get("rooms", [{}])[0]
            .get("rates", [{}])[0]
            .get("boardName"),
            "net": hotel.get("rooms", [{}])[0].get("rates", [{}])[0].get("net"),
        }
        normalized_hotels.append(normalized_hotel)

    return {"hotels": normalized_hotels}


def get_hotel_availability():
    """Fetch hotel availability from Hotelbeds API."""
    print("Calling Hotelbeds")
    try:
        data = request.json
        validated_data = HotelBedsRequestSchema().load(data)
        hotelbeds_request = transform_to_hotelbeds_request(validated_data)

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
            f"Hotelbeds response content (truncated): {str(response.content)[:2000]}..."
        )

        if response.status_code == 200:
            response_json = response.json()
            normalized_response = normalize_hotelbeds_response(response_json)
            return jsonify(normalized_response), 200
        else:
            return (
                jsonify({"error": f"Hotelbeds API error: {response.status_code}"}),
                response.status_code,
            )

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        print(f"Detailed error in get_hotel_availability: {str(e)}")
        return jsonify({"error": str(e)}), 500
