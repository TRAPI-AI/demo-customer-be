import requests
import hashlib
import time
import json

# Configuration - these should ideally come from environment variables or a config file
API_KEY = "HOTELBEDS_HOTEL_API_KEY"
SECRET = "HOTELBEDS_HOTEL_SECRET"
API_URL = "https://api.test.hotelbeds.com/hotel-api/v1/hotels"

def transform_request(frontend_payload):
    """
    Transforms the frontend request payload to the format required by Hotelbeds API.
    """
    transformed = {
        "stay": {
            "checkIn": frontend_payload["stay"]["checkIn"],
            "checkOut": frontend_payload["stay"]["checkOut"]
        },
        "occupancies": frontend_payload["occupancies"],
        "geolocation": frontend_payload["geolocation"]
    }
    return transformed

def generate_signature(api_key, secret):
    """
    Generates the X-Signature header value.
    """
    timestamp = str(int(time.time()))
    signature_string = f"{api_key}{secret}{timestamp}"
    sha_signature = hashlib.sha256(signature_string.encode()).hexdigest()
    return sha_signature, timestamp

def call_api(transformed_request):
    """
    Calls the Hotelbeds API with the transformed request and necessary headers.
    """
    signature, timestamp = generate_signature(API_KEY, SECRET)
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json",
        "Api-Key": API_KEY,
        "X-Signature": signature
    }
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(transformed_request))
    
    response.raise_for_status()  # Raises stored HTTPError, if one occurred.
    
    return response.json()

def normalize_response(api_response):
    """
    Normalizes the Hotelbeds API response to the unified response structure.
    """
    normalized = {
        "provider": "Hotelbeds",
        "hotels": []
    }
    
    hotels = api_response.get("hotels", {}).get("hotels", [])
    for hotel in hotels:
        normalized_hotel = {
            "code": hotel.get("code"),
            "name": hotel.get("name"),
            "categoryCode": hotel.get("categoryCode"),
            "categoryName": hotel.get("categoryName"),
            "destinationCode": hotel.get("destinationCode"),
            "destinationName": hotel.get("destinationName"),
            "zoneCode": hotel.get("zoneCode"),
            "zoneName": hotel.get("zoneName"),
            "latitude": hotel.get("latitude"),
            "longitude": hotel.get("longitude"),
            "rooms": [],
            "minRate": hotel.get("minRate"),
            "maxRate": hotel.get("maxRate"),
            "currency": hotel.get("currency"),
            "checkIn": api_response.get("checkIn"),
            "checkOut": api_response.get("checkOut")
        }
        
        for room in hotel.get("rooms", []):
            normalized_room = {
                "code": room.get("code"),
                "name": room.get("name"),
                "rates": []
            }
            for rate in room.get("rates", []):
                normalized_rate = {
                    "rateKey": rate.get("rateKey"),
                    "rateClass": rate.get("rateClass"),
                    "rateType": rate.get("rateType"),
                    "net": rate.get("net"),
                    "discount": rate.get("discount"),
                    "discountPCT": rate.get("discountPCT"),
                    "sellingRate": rate.get("sellingRate"),
                    "allotment": rate.get("allotment"),
                    "rateCommentsId": rate.get("rateCommentsId"),
                    "paymentType": rate.get("paymentType"),
                    "packaging": rate.get("packaging"),
                    "boardCode": rate.get("boardCode"),
                    "boardName": rate.get("boardName"),
                    "cancellationPolicies": rate.get("cancellationPolicies"),
                    "taxes": rate.get("taxes"),
                    "rooms": rate.get("rooms"),
                    "adults": rate.get("adults"),
                    "children": rate.get("children"),
                    "offers": rate.get("offers")
                }
                normalized_room["rates"].append(normalized_rate)
            normalized_hotel["rooms"].append(normalized_room)
        
        normalized["hotels"].append(normalized_hotel)
    
    return normalized