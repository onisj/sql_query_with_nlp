# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY src/ ./src/

COPY src/ /app

# Copy .env file
COPY .env .env

# Expose the port the app runs on
EXPOSE 8501 5000

# Command to run the application
CMD ["streamlit", "run", "src/app.py"]
