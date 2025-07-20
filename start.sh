#!/bin/bash

echo "Starting Data Analyst Agent..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo "Starting server on port ${PORT:-8000}..."
python main.py
