# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install cron and sudo
RUN apt-get update 
RUN apt-get install -y cron sudo

# Copy the rest of the application code into the container
COPY . /app/

# Run necessary scripts 
RUN python scripts/restartCronjob.py
RUN python scripts/start.py

# Start cron and the Django development server
CMD cron && python manage.py runserver 0.0.0.0:8000
