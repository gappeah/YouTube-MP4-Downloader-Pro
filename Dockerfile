# Use the official Python 3.13.1 image as the base
FROM python:3.13.1-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg (required for moviepy)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . .

# Set the entry point for the container
ENTRYPOINT ["python", "app.py"]