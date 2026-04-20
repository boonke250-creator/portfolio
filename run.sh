#!/bin/bash

echo "Starting Portfolio Admin Dashboard..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Install dependencies
echo "Checking dependencies..."
pip install -r requirements.txt -q

# Start Flask backend in background
python3 app.py &
FLASK_PID=$!
sleep 2

# Start HTTP server in background
python3 -m http.server 8000 &
SERVER_PID=$!

echo ""
echo "========================================"
echo "Flask Backend: http://localhost:5000"
echo "Portfolio: http://localhost:8000/boonke.html"
echo "Admin: Press Ctrl+Shift+A on the site"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for both processes
wait $FLASK_PID $SERVER_PID
