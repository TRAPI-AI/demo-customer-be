"""duffel_stays.py"""

import os
import requests
from flask import jsonify
from marshmallow import ValidationError
from ..schemas.duffel.duffel_search_schema import DuffelRequestSchema

DUFFEL_API_URL = "https://api.duffel.com/stays/search"

def transform_to_duffel_request(frontend_data):
    """Transform frontend request data to Duffel API request format."""
    stay = frontend_data["stay"]
    occupancies = frontend_data["occupancies"]
    geolocation = frontend_data["geolocation"]
    
    duffel_request = {
        "data": {
            "rooms": occupancies[0]["rooms"],
            "location": {
                "radius": geolocation["radius"],
                "geographic_coordinates": {
                    "longitude": geolocation["longitude"],
                    "latitude": geolocation["latitude"]
                }
            },
            "check_in_date": stay["checkIn"],
            "check_out_date": stay["checkOut"],
            "guests": [{"type": "adult"} for _ in range(occupancies[0]["adults"])]
        }
    }
    return duffel_request

def normalize_duffel_response(response_json):
    """Normalize Duffel API response to a consistent format."""
    results = response_json.get("data", {}).get("results", [])
    normalized_hotels = []
    
    for hotel in results:
        normalized_hotel = {
            "id": hotel.get("id"),
            "name": hotel.get("name"),
            "check_in_date": hotel.get("check_in_date"),
            "check_out_date": hotel.get("check_out_date"),
            "cheapest_rate_total_amount": hotel.get("cheapest_rate_total_amount"),
            "cheapest_rate_currency": hotel.get("cheapest_rate_currency"),
            "location": hotel.get("location", {}),
            "amenities": hotel.get("amenities", []),
            "photos": [photo.get("url") for photo in hotel.get("photos", [])],
            "rating": hotel.get("rating"),
            "review_score": hotel.get("review_score"),
            # Add more fields as needed
        }
        normalized_hotels.append(normalized_hotel)
    
    return {"hotels": normalized_hotels}

def search_duffel_stays(frontend_data):
    """Fetch hotel availability from Duffel API."""
    try:
        # Validate and transform request
        schema = DuffelRequestSchema()
        validated_data = schema.load(frontend_data)
        duffel_request = transform_to_duffel_request(validated_data)
        
        headers = {
            "Accept-Encoding": "gzip",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Duffel-Version": "v2",
            "Authorization": f"Bearer {os.getenv('DUFFEL_STAYS_API_KEY')}",
        }
        
        response = requests.post(DUFFEL_API_URL, headers=headers, json=duffel_request, timeout=10)
        
        if response.status_code == 200:
            response_json = response.json()
            normalized_response = normalize_duffel_response(response_json)
            return normalized_response
        else:
            return {"error": f"Duffel API error: {response.status_code}"}
    
    except ValidationError as err:
        return {"errors": err.messages}
    except Exception as e:
        return {"error": str(e)}

# To enable asynchronous calls
import asyncio
from functools import partial

async def search_duffel_stays_async(duffel_request):
    loop = asyncio.get_event_loop()
    func = partial(search_duffel_stays, duffel_request)
    return await loop.run_in_executor(None, func)