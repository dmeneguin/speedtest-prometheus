# Start from the official Python image
FROM python:3.11-slim

ENV APP_PORT=8000
ENV POLLING_INTERVAL_MINUTES=15

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script(s)
COPY connection_test.py .

# Set the default command to run your script
CMD ["python", "connection_test.py"]