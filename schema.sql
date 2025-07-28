
CREATE TABLE events (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	location VARCHAR(200) NOT NULL, 
	start_time DATETIME NOT NULL, 
	end_time DATETIME NOT NULL, 
	max_capacity INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
)

;


CREATE TABLE attendees (
	id INTEGER NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	event_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(event_id) REFERENCES events (id)
)

;

