from flask import request
from flask_smorest import Blueprint,abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from sqlalchemy import and_
from datetime import datetime
from db import db
from models import EventModel,AttendeeModel
from schemas import AttendeeSchema,ResponseAttedeeSchema,EventSchema,PaginationAttendeeSchema
from zoneinfo import ZoneInfo,available_timezones
from werkzeug.exceptions import NotFound
from zoneinfo._common import ZoneInfoNotFoundError

blp=Blueprint('events',__name__,'operation on events')

@blp.route('/events')
class Events(MethodView):

    @blp.response(200,EventSchema(many=True))
    def get(self):
        upcoming_events=[]
        attendee_timezone=request.headers.get('timezone','Asia/Kolkata')
        try:
            attendee_timezone=ZoneInfo(attendee_timezone)
        except ZoneInfoNotFoundError as e:
            abort(404,message='time zone not found')

        events= EventModel.query.all()
        for event in events:
            event.start_time=event.start_time.astimezone(attendee_timezone)
            event.end_time=event.end_time.astimezone(attendee_timezone)
            if event.start_time >= datetime.now(attendee_timezone):
                upcoming_events.append(event)
        if upcoming_events:
            return upcoming_events
        else:
            abort(404,message='No upcoming events found')
        
    @blp.arguments(EventSchema)
    @blp.response(201,EventSchema)
    def post(self,new_event):
        time_zone=ZoneInfo(new_event.get('timezone','Asia/Kolkata'))
        if time_zone not in available_timezones():
            time_zone=ZoneInfo('Asia/Kolkata')
        start_time_local=new_event['start_time'].replace(tzinfo=time_zone)
        end_time_local=new_event['end_time'].replace(tzinfo=time_zone)

        start_time_utc = start_time_local.astimezone(ZoneInfo("UTC"))
        end_time_utc = end_time_local.astimezone(ZoneInfo("UTC"))
        new_event['start_time']=start_time_utc  
        new_event['end_time']=end_time_utc
        new_event=EventModel(**new_event)
        try:
            db.session.add(new_event)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message='Error occured while creating event')
        new_event.start_time=start_time_local
        new_event.end_time=end_time_local
        return new_event
    
@blp.route('/events/<string:event_id>/register')
class EventRegister(MethodView):

    @blp.arguments(AttendeeSchema)
    @blp.response(201,AttendeeSchema)
    def post(self,attendee,event_id):
        event=EventModel.query.get(event_id)
        if event:
            exsiting_attendee_for_event=AttendeeModel.query.filter(and_(AttendeeModel.email==attendee['email'],AttendeeModel.event_id==event_id)).first()
            if not exsiting_attendee_for_event:
                if event.attendees.count() < event.max_capacity:
                    new_attendee=AttendeeModel(**attendee,event_id=event_id)
                    try:
                        db.session.add(new_attendee)
                        db.session.commit()
                    except SQLAlchemyError as e:
                        abort(500,message='Error occuured while registering the attendee with given event')
                    return new_attendee
                else:
                    abort(404,message='Event is fully booked. No more seats are available.')
            else:
                abort(404,message='User has already registered for the given event')
        else:
            abort(404,message='Even does not exist for the given id')


@blp.route('/events/<string:event_id>/attendees')
class EventAttendees(MethodView):
    @blp.arguments(PaginationAttendeeSchema,location='query')
    @blp.response(200,ResponseAttedeeSchema)
    def get(self,query_params,event_id):
        per_page=query_params.get('perpage')
        page=query_params.get('page')
     
        event=EventModel.query.get(event_id)
        if event:
            try:
                pagination=event.attendees.paginate(page=page,per_page=per_page,error_out=True)
                total_attendees={
                    'page':pagination.page,
                    'per_page':pagination.per_page,
                    'total_items':pagination.total,
                    'total_pages':pagination.pages,
                    'next_page':pagination.next_num if pagination.has_next else None,
                    'prev_page':pagination.prev_num if pagination.has_prev else None,
                    'attendees':AttendeeSchema(many=True).dump(pagination.items)
                }
            except NotFound as e:
                abort(404,message='Given page does not exist')
            if len(pagination.items) > 0:
                return total_attendees
            else:
                abort(404,message='No attendes resigtered for the given event')
        else:
            abort(404,message='No events found with given event id')