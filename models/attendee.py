from db import db

class AttendeeModel(db.Model):
    __tablename__='attendees'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False,unique=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    event_id=db.Column(db.Integer,db.ForeignKey('events.id'),nullable=False,unique=False)
    events=db.relationship('EventModel',back_populates='attendees')
