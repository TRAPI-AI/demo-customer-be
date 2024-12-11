"""routes.py"""

from flask import Blueprint, request
from .providers.hotelbeds_hotels import get_hotel_availability
from .providers.duffel_stays import search_duffel_stays
from .utils.aggregator import get_unified_response

router = Blueprint("router", __name__)

@router.route("/hotelbeds-hotels-booking-hotel-availability", methods=["POST"])
def hotel_availability():
    """Hotel Availability Search"""
    return get_hotel_availability()

@router.route("/unified-endpoint", methods=["POST"])
def unified_endpoint():
    """Unified Endpoint for Multiple Providers"""
    return get_unified_response(request.json)