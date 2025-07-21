# Use a minimal Python 3 image
FROM python:3.11-slim

# Set environment variable to flush logs immediately
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Copy all files from current directory to the container
COPY . .

# Install required Python packages
RUN pip install flask requests

# Expose port 8080 for the User Server
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]
