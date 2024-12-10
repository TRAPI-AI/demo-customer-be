"""aggregator.py"""

import concurrent.futures
from flask import jsonify
from app.providers.hotelbeds_hotels import get_hotel_availability as get_hotelbeds_availability
from app.providers.duffel_stays import get_duffel_availability as get_duffel_availability


def unified_response(hotelbeds_data, duffel_data):
    """Combine responses from all providers into a unified format."""
    unified = {
        "hotels": []
    }

    if hotelbeds_data.get("hotels"):
        unified["hotels"].extend(hotelbeds_data["hotels"])

    if duffel_data.get("hotels"):
        unified["hotels"].extend(duffel_data["hotels"])

    return unified


def get_unified_hotel_availability():
    """Fetch hotel availability from all providers and unify the response."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_hotelbeds = executor.submit(get_hotelbeds_availability_internal)
        future_duffel = executor.submit(get_duffel_availability_internal)

        hotelbeds_result = future_hotelbeds.result()
        duffel_result = future_duffel.result()

    # Handle errors from providers
    unified_errors = {}
    unified_hotels = []

    if hotelbeds_result[1] == 200:
        hotelbeds_data = hotelbeds_result[0].json()
        unified_hotels.extend(hotelbeds_data.get("hotels", []))
    else:
        unified_errors["hotelbeds"] = hotelbeds_result[0].json().get("error", "Unknown error")

    if duffel_result[1] == 200:
        duffel_data = duffel_result[0].json()
        unified_hotels.extend(duffel_data.get("hotels", []))
    else:
        unified_errors["duffel"] = duffel_result[0].json().get("error", "Unknown error")

    if unified_errors:
        return jsonify({"errors": unified_errors, "hotels": unified_hotels}), 207  # 207 Multi-Status

    return jsonify({"hotels": unified_hotels}), 200


def get_hotelbeds_availability_internal():
    """Internal call to Hotelbeds provider without HTTP context."""
    with app.test_request_context(json=request.get_json()):
        return get_hotelbeds_availability()


def get_duffel_availability_internal():
    """Internal call to Duffel Stays provider without HTTP context."""
    with app.test_request_context(json=request.get_json()):
        return get_duffel_availability()

---