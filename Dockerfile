# Use a specific version of the Python image to ensure consistency.
# slim-buster version is smaller and more secure than the full image.
FROM python:3.8-slim-buster

# Set environment variables to:
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Prevent Python from writing pyc files to disk (equivalent to python -B option).
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container to /app.
WORKDIR /app

# Install dependencies:
# Copy only the requirements.txt file to leverage Docker cache,
# install the Python dependencies, then copy the rest of the app.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . .

# Non-root User:
# Create a user to run the application safely (not as root).
# This is a security best practice in Docker containers.
RUN adduser --disabled-password --gecos '' myuser
USER myuser

# Make port 5000 available to the world outside this container.
EXPOSE 5000

# Run the application:
# Use the exec form of CMD to help Docker send the correct signals to the Python process.
CMD ["python", "run.py"]
