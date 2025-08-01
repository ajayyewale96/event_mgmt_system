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

# Setup Instructions

Setup Instructions
------------------

Step 1: Clone the Repository via Git Bash
-----------------------------------------
- git clone https://github.com/ajayyewale96/event_mgmt_system.git
- cd event_mgmt_system

Step 2: Create a Virtual Environment
------------------------------------
python -m venv venv

- For UNIX/macOS:
  source venv/bin/activate

- For Windows:
  venv\Scripts\activate.bat

Step 3: Install the Required Python Packages
--------------------------------------------
pip install -r requirements.txt

Step 4: Run the Application
---------------------------
flask run

App will be running at: http://localhost:5000


---

# Assumptions

- The user has to provide the timezone in the header of the request for both posting the event and gettin the list of events  if no timezone is provided the code default to IST timezone for both event creation and display of event.Events are stored in UTC format in the sqlite db.
- No two registrations for a given event should be  present for the same email_id
- Here I am also assuming that user can register for as many events as possible even though there might be overlap as in the end user will only be able to be present for one event physically.
- The events registered for the same location should not overlap for the given start time and end time
- User has to given in the page number and number of attendees per_page as query params to see the attendee list for a given event .If no values given a default value of page=1 and per_page=10 is assumed
- 
---
# Sample API Requests (via `curl`)

---

### 1) `POST /events`

```bash
curl -X POST http://localhost:5000/events \
-H "Content-Type: application/json" \
-d '{
  "name": "Omnify Summit 2025",
  "location": "Pune",
  "start_time": "2025-08-10T10:00:00",
  "end_time": "2025-08-10T17:00:00",
  "max_capacity": 300
}'
```

---

### 2) `GET /events`

```bash
curl http://localhost:5000/events
```

---

### 3) `POST /events/{event_id}/register`

```bash
curl -X POST http://localhost:5000/events/1/register \
-H "Content-Type: application/json" \
-d '{
  "name": "Ajay Yewale",
  "email": "ajayyewle8@gmail.com"
}'
```

---

### 4) `GET /events/{event_id}/attendees`

```bash
curl http://localhost:5000/events/1/attendees?page=1&perpage=10
```
