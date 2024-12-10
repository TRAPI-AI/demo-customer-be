"""duffel_stays.py"""

import os
import requests
from flask import request, jsonify
from marshmallow import ValidationError
from app.schemas.duffel.duffel_search_schema import DuffelSearchRequestSchema


def transform_duffel_request(frontend_data):
    """Transform frontend request data to Duffel Stays API request format."""
    stay = frontend_data["stay"]
    occupancies = frontend_data["occupancies"]
    geolocation = frontend_data["geolocation"]

    check_in_date = stay["checkIn"]
    check_out_date = stay["checkOut"]

    # Assuming single room and adult for simplicity; adjust as needed
    guests = []
    for occupancy in occupancies:
        for _ in range(occupancy["adults"]):
            guests.append({"type": "adult"})
        for _ in range(occupancy["children"]):
            guests.append({"type": "child"})

    duffel_request = {
        "data": {
            "rooms": occupancies[0]["rooms"],
            "location": {
                "radius": geolocation["radius"],
                "geographic_coordinates": {
                    "longitude": geolocation["longitude"],
                    "latitude": geolocation["latitude"],
                },
            },
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "guests": guests,
        }
    }

    return duffel_request


def normalize_duffel_response(response_json):
    """Normalize Duffel Stays API response to a consistent format."""
    results = response_json.get("data", {}).get("results", [])
    normalized_hotels = []

    for result in results:
        accommodation = result.get("accommodation", {})
        rooms = accommodation.get("rooms", [])
        if not rooms:
            continue
        room = rooms[0]
        rates = room.get("rates", [])
        if not rates:
            continue
        rate = rates[0]

        normalized_hotel = {
            "code": accommodation.get("id"),
            "name": accommodation.get("name"),
            "checkIn": result.get("check_in_date"),
            "checkOut": result.get("check_out_date"),
            "cheapestRateTotalAmount": rate.get("total_amount"),
            "cheapestRateCurrency": rate.get("total_currency"),
            "rateClass": rate.get("payment_type"),
            "availableRooms": rate.get("quantity_available"),
            "rating": accommodation.get("rating"),
            "location": accommodation.get("location", {}),
            "amenities": accommodation.get("amenities", []),
        }
        normalized_hotels.append(normalized_hotel)

    return {"hotels": normalized_hotels}


def get_duffel_availability():
    """Fetch hotel availability from Duffel Stays API."""
    print("Calling Duffel Stays")
    try:
        data = request.json
        validated_data = DuffelSearchRequestSchema().load(data)
        duffel_request = transform_duffel_request(validated_data)

        api_key = os.getenv("DUFFEL_STAYS_API_KEY")
        headers = {
            "Accept-Encoding": "gzip",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Duffel-Version": "v2",
            "Authorization": f"Bearer {api_key}",
        }

        response = requests.post(
            "https://api.duffel.com/stays/search",
            headers=headers,
            json=duffel_request,
            timeout=10,
        )
        print(f"Duffel Stays response status: {response.status_code}")
        print(f"Duffel Stays response content (truncated): {str(response.content)[:2000]}...")

        if response.status_code == 200:
            response_json = response.json()
            normalized_response = normalize_duffel_response(response_json)
            return jsonify(normalized_response), 200
        else:
            return (
                jsonify({"error": f"Duffel Stays API error: {response.status_code}"}),
                response.status_code,
            )

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        print(f"Detailed error in get_duffel_availability: {str(e)}")
        return jsonify({"error": str(e)}), 500

---