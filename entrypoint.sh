#!/bin/sh
echo "Running DB migrations..."
flask db upgrade

echo "Starting the app..."
exec gunicorn --bind 0.0.0.0:5000 'app:create_app()'