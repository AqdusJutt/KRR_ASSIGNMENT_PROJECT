#!/bin/bash

# Start script for Multi-Agent Chat System

echo "========================================="
echo "Multi-Agent Chat System - Startup"
echo "========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    python setup_env.py
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================="
echo "Backend Setup Complete!"
echo "========================================="
echo ""
echo "To start the backend server:"
echo "  uvicorn main:app --reload --port 8000"
echo ""
echo "To start the console client:"
echo "  python console_client.py"
echo ""
echo "To run tests:"
echo "  python run_tests.py"
echo ""

