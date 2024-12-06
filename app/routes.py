"""routes.py"""

from flask import Blueprint
from .providers.hotelbeds import get_hotel_availability

router = Blueprint("router", __name__)


@router.route("/hotelbeds-hotels-booking-hotel-availability", methods=["POST"])
def hotel_availability():
    """Hotel Availability Search"""
    return get_hotel_availability()
