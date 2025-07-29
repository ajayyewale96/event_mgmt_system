from db import db

class EventModel(db.Model):
    __tablename__='events'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False,unique=False)
    location=db.Column(db.String(200),nullable=False,unique=False)
    start_time=db.Column(db.DateTime(timezone=True),nullable=False,unique=False)
    end_time=db.Column(db.DateTime(timezone=True),nullable=False,unique=False)
    max_capacity=db.Column(db.Integer,nullable=False,unique=False)
    attendees=db.relationship('AttendeeModel',back_populates='events',lazy='dynamic')