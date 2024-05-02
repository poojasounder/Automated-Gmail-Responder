# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Specify your e-mail address as the maintainer of the container image
LABEL maintainer="pooja3@pdx.edu"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment
RUN python3 -m venv env

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the playwright install command to download and install browsers
RUN npm install -g playwright && playwright install

# Expose port 8080 to the outside world
EXPOSE 8080

# Make the script executable
RUN chmod +x run.sh

# Run the script
CMD ["./run.sh"]