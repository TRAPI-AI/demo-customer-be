"""routes.py"""

from flask import Blueprint, request, jsonify
from .providers.hotelbeds_hotels import get_hotel_availability
from .utils.aggregator import get_unified_hotel_availability

router = Blueprint("router", __name__)

@router.route("/hotelbeds-hotels-booking-hotel-availability", methods=["POST"])
def hotel_availability():
    """Hotel Availability Search"""
    return get_hotel_availability()

@router.route("/unified-hotel-availability", methods=["POST"])
def unified_hotel_availability():
    """Unified Hotel Availability Search"""
    try:
        frontend_data = request.json
        unified_response = get_unified_hotel_availability(frontend_data)
        return jsonify(unified_response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500