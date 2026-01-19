FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libsmbclient-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY run.py .
COPY .env.example .env

# Create directories
RUN mkdir -p logs certs/app certs/metrics /tmp/policy-reader

# Expose ports
EXPOSE 8000 9090

# Run application
CMD ["python", "run.py"]
