# Use an official Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set the working directory
WORKDIR /app

# Install dependencies needed for compiling some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from the host to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the API port
EXPOSE $PORT

# Command to run the application using uvicorn
CMD if [ -z "$PORT" ]; then \
        uvicorn app:app --host 0.0.0.0 --port 8000; \
    else \
        uvicorn app:app --host 0.0.0.0 --port $PORT; \
    fi
