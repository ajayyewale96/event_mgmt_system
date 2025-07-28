from marshmallow import Schema,fields

class EventSchema(Schema):
    id=fields.Integer(dump_only=True)
    name=fields.String(required=True)
    location=fields.String(required=True)
    start_time=fields.DateTime(required=True)
    end_time=fields.DateTime(required=True)
    max_capacity=fields.Integer(required=True)

class AttendeeSchema(Schema):
    id=fields.Integer(dump_only=True)
    name=fields.String(required=True)
    email=fields.String(required=True)

class ResponseAttedeeSchema(AttendeeSchema):
    page=fields.Integer(dump_only=True)
    per_page=fields.Integer(dump_only=True)
    total_items=fields.Integer(dump_only=True)
    total_pages=fields.Integer(dump_only=True)
    next_page=fields.Integer(dump_only=True)
    prev_page=fields.Integer(dump_only=True)
    attendees=fields.List(fields.Nested(AttendeeSchema,dump_only=True))

class PaginationAttendeeSchema(Schema):
    page=fields.Integer(load_default=1)
    perpage=fields.Integer(load_default=10)