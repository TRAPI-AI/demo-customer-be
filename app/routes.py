"""routes.py"""

from flask import Blueprint
from .utils.aggregator import get_unified_hotel_availability

router = Blueprint("router", __name__)


@router.route("/unified-endpoint", methods=["POST"])
def unified_hotel_availability():
    """Unified Hotel Availability Search"""
    return get_unified_hotel_availability()

---