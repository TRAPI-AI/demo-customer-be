"""HotelBeds Search Schema"""

from marshmallow import Schema, fields


class StaySchema(Schema):
    """Schema for stay details including check-in and check-out dates."""

    checkIn = fields.Date(required=True, format="%Y-%m-%d")
    checkOut = fields.Date(required=True, format="%Y-%m-%d")


class OccupancySchema(Schema):
    """Schema for occupancy details including number of rooms, adults, and children."""

    rooms = fields.Integer(required=True)
    adults = fields.Integer(required=True)
    children = fields.Integer(required=True)


class GeolocationSchema(Schema):
    """Schema for geolocation details including latitude, longitude, radius, and unit."""

    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    radius = fields.Integer(required=True)
    unit = fields.String(required=True)


class HotelBedsRequestSchema(Schema):
    """Schema for HotelBeds request including stay, occupancies, and geolocation."""

    stay = fields.Nested(StaySchema, required=True)
    occupancies = fields.List(fields.Nested(OccupancySchema), required=True)
    geolocation = fields.Nested(GeolocationSchema, required=True)
