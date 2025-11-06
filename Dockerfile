# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy your project code into the container
COPY . /app/

# Run the development server
# We use 0.0.0.0 to listen for all connections, not just localhost
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
