# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create the data directory and copy mysql_conn.py
RUN mkdir -p /app/data
COPY data/mysql_conn.py /app/data/

# Run mysql_conn.py to download and save init.sql
RUN python /app/data/mysql_conn.py

# Check if init.sql file exists (for debugging)
RUN ls -l /app/data/init.sql

# Copy the source code into the container
COPY src/ /app/src/

# Copy the data folder for the database initialization script
COPY data/ /app/data/

# Expose ports for Streamlit and Flask
EXPOSE 8501 5000

# Command to run the Streamlit application
CMD ["streamlit", "run", "src/app_st.py", "--server.port", "8501"]

# Command to run the Flask application (commented out for now)
# CMD ["flask", "run", "--host=0.0.0.0", "--port", "5000"]
