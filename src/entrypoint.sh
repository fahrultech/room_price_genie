#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate
python manage.py load_data_from_csv

# Start the server
echo "Starting the web server..."
exec "$@"
