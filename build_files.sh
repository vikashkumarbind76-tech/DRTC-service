#!/bin/bash
echo "=== DRTC SERVICE VERCEL BUILD START ==="

# Install dependencies
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput --clear

# Run database migrations
python3 manage.py migrate --noinput

echo "=== DRTC SERVICE VERCEL BUILD COMPLETE ==="
