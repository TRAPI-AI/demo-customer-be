"""routes.py"""

from flask import Blueprint, request, jsonify
from .providers.hotelbeds_hotels import get_hotel_availability
from .providers.duffel_flights import list_duffel_flight_offers

router = Blueprint("router", __name__)

@router.route("/hotelbeds-hotels-booking-hotel-availability", methods=["POST"])
def hotel_availability():
    """Hotel Availability Search"""
    return get_hotel_availability()

@router.route("/duffel-flights-list-offers", methods=["POST"])
def duffel_flights_list_offers():
    """Duffel Flights List Offers"""
    data = request.get_json()
    return list_duffel_flight_offers(data)