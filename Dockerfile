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

# NEW: Collect all static files (CSS, JS) into one folder
# We must use the correct path to your manage.py
RUN python taxproject/manage.py collectstatic --noinput

# NEW: Run the Gunicorn server
# It will run the 'wsgi.py' file located in your 'taxproject' folder
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "taxproject.wsgi:application"]