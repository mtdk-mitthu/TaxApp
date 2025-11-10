# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create and set the working directory
RUN mkdir -p /app
COPY . /app/

# Set the working directory to the project folder (where manage.py is)
WORKDIR /app/taxproject

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# This is the default command to run Gunicorn
CMD ["gunicorn", "taxproject.wsgi:application", "--bind", "0.0.0.0:8000"]