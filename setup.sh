#!/bin/bash

# Cinema Management System - Quick Start Script for macOS/Linux

echo "================================================"
echo "  Cinema Management System - Setup Script"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    exit 1
fi

echo "[1/6] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
fi

echo "[2/6] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "[3/6] Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/6] Running migrations..."
python manage.py makemigrations
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to run migrations"
    exit 1
fi

echo ""
echo "[5/6] Creating superuser..."
echo "Please enter admin credentials:"
python manage.py createsuperuser

if [ $? -ne 0 ]; then
    echo "NOTE: Superuser creation aborted or failed"
fi

echo ""
echo "[6/6] Setup complete!"
echo ""
echo "================================================"
echo "  Next Steps:"
echo "================================================"
echo ""
echo "To start the development server, run:"
echo "    python manage.py runserver"
echo ""
echo "Then open your browser and go to:"
echo "    http://localhost:8000"
echo ""
echo "Admin panel:"
echo "    http://localhost:8000/admin"
echo ""
echo "To load sample data (optional):"
echo "    python manage.py shell < seed_data.py"
echo ""
echo "================================================"
echo ""
