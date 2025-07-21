# Use a minimal Python image
FROM python:3.11-slim

# Set environment variable to show real-time logs
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy all local files into the container
COPY . .

# Install required packages
RUN pip install flask requests

# Expose HTTP port
EXPOSE 9090

# Run the Flask app
CMD ["python", "app.py"]
