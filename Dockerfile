# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Specify your e-mail address as the maintainer of the container image
LABEL maintainer="pooja3@pdx.edu"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the container with environment variable for OpenAI API key
CMD ["sh", "-c", "python injection.py && uvicorn llm:app --reload"]

