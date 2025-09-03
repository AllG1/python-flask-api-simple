#!/bin/bash
echo "Starting application..."

# Run application
poetry run uwsgi --ini /workspace/uwsgi.ini 

# Keep the container running
tail -f /dev/null

# # Clean up processes
# trap 'kill $(jobs -p)' EXIT
# wait