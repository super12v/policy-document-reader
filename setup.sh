#!/bin/bash

# Policy Document Reader Setup Script

echo "Setting up Policy Document Reader MCP Server..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create directories
echo "Creating directories..."
mkdir -p logs certs/app certs/metrics /tmp/policy-reader

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

echo ""
echo "Setup complete!"
echo ""
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "Or with Docker:"
echo "  docker-compose up --build"
