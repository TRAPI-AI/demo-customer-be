"""Duffel Search Schema"""

from marshmallow import Schema, fields, validate

class GuestSchema(Schema):
    """Schema for guests."""
    type = fields.String(required=True, validate=validate.OneOf(["adult", "child"]))

class LocationSchema(Schema):
    """Schema for location details."""
    radius = fields.Integer(required=True)
    geographic_coordinates = fields.Dict(
        keys=fields.Str(),
        values=fields.Float(),
        required=True,
        validate=lambda x: "latitude" in x and "longitude" in x
    )

class DuffelRequestSchema(Schema):
    """Schema for Duffel request including rooms, location, dates, and guests."""
    data = fields.Dict(required=True)
    
    # Further validation can be added as needed