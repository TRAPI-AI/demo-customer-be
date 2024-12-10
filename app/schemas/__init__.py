"""schemas/__init__.py"""

from .hotelbeds.hotelbeds_search_schema import HotelBedsRequestSchema
from .duffel.duffel_search_schema import DuffelSearchRequestSchema

__all__ = [
    "HotelBedsRequestSchema",
    "DuffelSearchRequestSchema",
]

---