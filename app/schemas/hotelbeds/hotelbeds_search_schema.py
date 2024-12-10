"""HotelBeds Search Schema"""

from marshmallow import Schema, fields


class StaySchema(Schema):
    checkIn = fields.Date(required=True, format="%Y-%m-%d")
    checkOut = fields.Date(required=True, format="%Y-%m-%d")


class OccupancySchema(Schema):
    rooms = fields.Integer(required=True)
    adults = fields.Integer(required=True)
    children = fields.Integer(required=True)


class GeolocationSchema(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    radius = fields.Integer(required=True)
    unit = fields.String(required=True)


class HotelBedsRequestSchema(Schema):
    stay = fields.Nested(StaySchema, required=True)
    occupancies = fields.List(fields.Nested(OccupancySchema), required=True)
    geolocation = fields.Nested(GeolocationSchema, required=True)
