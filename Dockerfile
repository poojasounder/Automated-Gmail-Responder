# Use a slim Python base layer
FROM python:3.9-slim

# Specify your e-mail address as the maintainer of the container image
LABEL maintainer="wuchang@pdx.edu"

# Copy the contents of the current directory into the container directory /app
COPY . /app

# Set the working directory of the container to /app
WORKDIR /app

# Create a virtual environment
RUN python3 -m venv env

# Install the Python packages specified by requirements.txt into the container
RUN env/bin/pip install -r requirements.txt

# Set the parameters to the program
CMD env/bin/gunicorn --bind :$PORT --workers 1 --threads 8 app:app
