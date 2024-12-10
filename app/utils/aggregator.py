"""aggregator.py"""

import os
import time
from flask import jsonify
from .providers.hotelbeds_hotels import generate_signature
from .providers.hotelbeds_hotels import transform_to_hotelbeds_request
from .providers.hotelbeds_hotels import get_hotel_availability as hotelbeds_provider
from .providers.duffel_stays import fetch_duffel_stays

def transform_duffel_request(frontend_data):
    """Transform frontend request data to Duffel Stays API request format."""
    return {
        "data": {
            "rooms": frontend_data.get("rooms", 1),
            "location": {
                "radius": frontend_data.get("location", {}).get("radius", 1),
                "geographic_coordinates": {
                    "longitude": frontend_data.get("location", {}).get("geographic_coordinates", {}).get("longitude", 1.0),
                    "latitude": frontend_data.get("location", {}).get("geographic_coordinates", {}).get("latitude", 1.0),
                },
            },
            "check_in_date": frontend_data.get("stay", {}).get("checkIn", ""),
            "check_out_date": frontend_data.get("stay", {}).get("checkOut", ""),
            "guests": frontend_data.get("occupancies", [{"type": "adult"}]),
        }
    }

def call_hotelbeds_api(frontend_data):
    """Call Hotelbeds API with transformed request."""
    try:
        transformed_request = transform_to_hotelbeds_request(frontend_data)
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
            json=transformed_request,
            timeout=10,
        )
        print(f"Hotelbeds response status: {response.status_code}")
        print(f"Hotelbeds response content (truncated): {str(response.content)[:200]}...")
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Hotelbeds API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def call_duffel_api(frontend_data):
    """Call Duffel Stays API with transformed request."""
    try:
        transformed_request = transform_duffel_request(frontend_data)
        duffel_response = fetch_duffel_stays(transformed_request)
        return duffel_response
    except Exception as e:
        return {"error": str(e)}

def normalize_hotelbeds_response(response):
    """Normalize Hotelbeds API response to unified structure."""
    if "error" in response:
        return {"provider": "hotelbeds", "error": response["error"]}
    
    # Example normalization; adjust based on actual Hotelbeds response structure
    normalized = {
        "provider": "hotelbeds",
        "results": response.get("hotels", []),
    }
    return normalized

def normalize_duffel_response(response):
    """Normalize Duffel Stays API response to unified structure."""
    if "error" in response:
        return {"provider": "duffel", "error": response["error"]}

    # Example normalization based on provided Duffel response structure
    data = response.get("data", {})
    results = data.get("results", [])
    normalized_results = []

    for item in results:
        normalized_item = {
            "id": item.get("id"),
            "name": item.get("name"),
            "check_in_date": item.get("check_in_date"),
            "check_out_date": item.get("check_out_date"),
            "cheapest_rate_total_amount": item.get("cheapest_rate_total_amount"),
            "cheapest_rate_currency": item.get("cheapest_rate_currency"),
            "location": item.get("location", {}),
            "amenities": item.get("amenities", []),
            # Add more fields as needed
        }
        normalized_results.append(normalized_item)

    normalized = {
        "provider": "duffel",
        "results": normalized_results,
    }
    return normalized

def get_unified_hotel_availability(frontend_data):
    """Fetch and unify hotel availability from all providers."""
    hotelbeds_response = call_hotelbeds_api(frontend_data)
    duffel_response = call_duffel_api(frontend_data)

    normalized_hotelbeds = normalize_hotelbeds_response(hotelbeds_response)
    normalized_duffel = normalize_duffel_response(duffel_response)

    unified_results = {
        "data": {
            "results": []
        },
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    # Merge Hotelbeds results
    if "error" not in normalized_hotelbeds:
        unified_results["data"]["results"].extend(normalized_hotelbeds.get("results", []))
    else:
        unified_results["data"]["results"].append({
            "provider": normalized_hotelbeds["provider"],
            "error": normalized_hotelbeds["error"]
        })

    # Merge Duffel results
    if "error" not in normalized_duffel:
        unified_results["data"]["results"].extend(normalized_duffel.get("results", []))
    else:
        unified_results["data"]["results"].append({
            "provider": normalized_duffel["provider"],
            "error": normalized_duffel["error"]
        })

    return unified_results