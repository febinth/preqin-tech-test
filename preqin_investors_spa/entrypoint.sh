#!/bin/sh

# Run the tests
echo "Running tests..."
python manage.py test

# Check if tests passed
if [ $? -ne 0 ]; then
    echo "Tests failed, exiting."
    exit 1
fi

# Start the server
echo "Starting the server..."
exec "$@"