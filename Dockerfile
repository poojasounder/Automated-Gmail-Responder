# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Specify your e-mail address as the maintainer of the container image
LABEL maintainer="pooja3@pdx.edu"

#RUN apt-get update -y
#RUN apt-get install -y python3-pip


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment
RUN python3 -m venv env

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

CMD ["uvicorn", "llm:app", "--reload", "--port", "8000"]

