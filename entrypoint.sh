#!/bin/sh
echo "Running DB migrations..."
flask db upgrade

echo "Starting the app..."
exec flask run