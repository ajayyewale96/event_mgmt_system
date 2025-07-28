from db import db
from app import create_app
from models.event import EventModel
from models.attendee import AttendeeModel
from sqlalchemy.schema import CreateTable

with create_app().app_context():
    with open("schema.sql", "w") as f:
        for model in [EventModel, AttendeeModel]:
            f.write(str(CreateTable(model.__table__).compile(db.engine)))
            f.write(";\n\n")
