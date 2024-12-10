"""Duffel Search Schema"""

from marshmallow import Schema, fields, validate


class GeographicCoordinatesSchema(Schema):
    """Schema for geographic coordinates."""
    longitude = fields.Float(required=True)
    latitude = fields.Float(required=True)


class LocationSchema(Schema):
    """Schema for location details."""
    radius = fields.Integer(required=True, validate=validate.Range(min=1))
    geographic_coordinates = fields.Nested(GeographicCoordinatesSchema, required=True)


class GuestSchema(Schema):
    """Schema for guest details."""
    type = fields.String(required=True, validate=validate.OneOf(["adult", "child"]))


class DuffelSearchRequestSchema(Schema):
    """Schema for Duffel Stays search request."""

    stay = fields.Nested(
        Schema.from_dict({
            "checkIn": fields.Date(required=True, format="%Y-%m-%d"),
            "checkOut": fields.Date(required=True, format="%Y-%m-%d"),
        }),
        required=True,
    )
    occupancies = fields.List(
        fields.Nested(
            Schema.from_dict({
                "rooms": fields.Integer(required=True, validate=validate.Range(min=1)),
                "adults": fields.Integer(required=True, validate=validate.Range(min=1)),
                "children": fields.Integer(required=True, validate=validate.Range(min=0)),
            })
        ),
        required=True,
        validate=validate.Length(min=1),
    )
    geolocation = fields.Nested(LocationSchema, required=True)

---