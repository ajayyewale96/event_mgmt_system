# Event Management System REST API

This project is a mini Event Management System built using python,flask(rest api development),
flask-smorest(extension for flask which supports Marshmalllow schema for data validation,support for swagger/OpenAPI documentation,blueprints for code modularity),
SQLite(db storage),SQLAlchemy and flask-sqlalchemy for ORM.

THis project provides the following functionilities to the user:
- Create events
- Register attendees for events
- View upcoming events
- View attendee lists for a given event
- Prevent overbooking and duplicate registrations
- Manage timezones and paginated attendee listings

---

# Features Implemented

- Create and list events
- Register attendees with validation (no duplicates, max capacity)
- View attendees per event (with pagination)
- Timezone-aware datetime handling for viewing the upcoming events based on user's timezone(default: IST)
- Clean separation of models, routes, and logic
- Swagger/OpenAPI docs (via flask-smorest)

---

# Tech Stack

| Component     | Technology         |
|---------------|------------------  | 
| Language      | Python 3.13.2      |
| Framework     | Flask              |
| ORM           | SQLAlchemy         |
| Database      | SQLite             |
| Timezone      | zoneinfo           |
| Docs          | Swagger (flask-smorest) |

---
# Project folder structure

├── event_mgmt_system/
│   ├── .flask_env
│   ├── app.py
│   ├── db.py
│   ├── requirements.txt
│   ├── schemas.py
│   ├── instance/
│   │   ├── data.db
│   ├── models/
│   │   ├── __init__.py
│   │   ├── attendee.py
│   │   ├── event.py
│   ├── resources/
│   │   ├── event.py

---

# Setup Instructions

Step 1: Clone the Repository via git bash
git clone https://github.com/ajayyewale96/event_mgmt_system.git
cd event_mgmt_system

Step 2: Create virtual env
python -m venv venv
UNIX: venv/bin/activate  
Windows: venv\Scripts\activate.bat

Step 3: Install the python packages
pip install -r requirements.txt

Step 4:Run the app
flask run
App runs at: http://localhost:5000

---

# Assumptions

1)The user has to provide the timezone in the header of the request if no timezone is provided the code default to IST timezone for event creation.
2)As per the requirement docx and I quote "Prevent duplicate registrations for the same email". As per my understanding of this statement I am assuming that same user should 
not register again for the same event i.e  no two registrations should be  present for the same email_id
3)Here I am also assuming that user can register for as many events as possible even though there might be overlap as in the end user will only be able to be present for one event physically.
4)The events registered for the same location should not overlap for the given start time and end time

---
# Sample API Requests (via curl)

1)POST /events

curl -X POST http://localhost:5000/events \
-H "Content-Type: application/json" \
-d '{
  "name": "Omnify Summit 2025",
  "location": "Pune",
  "start_time": "2025-08-10T10:00:00",
  "end_time": "2025-08-10T17:00:00",
  "max_capacity": 300
}'


2)GET /events

curl http://localhost:5000/events


3)POST /events/{event_id}/register

curl -X POST http://localhost:5000/events/1/register \
-H "Content-Type: application/json" \
-d '{
  "name": "Ajay Yewale",
  "email": "ajayyewle8@gmail.com"
}'


4)GET /events/{event_id}/attendees

curl http://localhost:5000/events/1/attendees?page=1&perpage=10
