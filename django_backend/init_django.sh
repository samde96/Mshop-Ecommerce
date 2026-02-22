#!/bin/bash

# Django Backend Initialization Script
# This script sets up the Django environment and initializes the database

set -e

echo "=========================================="
echo "M-Shop Django Backend Setup"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.10+"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please update .env with your configuration"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if no superuser exists
echo "Checking for superuser..."
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    print("Creating superuser...")
    User.objects.create_superuser('admin', 'admin@mshop.local', 'admin123')
    print("Superuser created: admin / admin123")
else:
    print("Superuser already exists")
END

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver 0.0.0.0:8000"
echo ""
echo "To migrate data from MongoDB, run:"
echo "  python migrate_from_mongodb.py"
echo ""
echo "Access admin at: http://localhost:8000/admin/"
echo "API at: http://localhost:8000/api/"
