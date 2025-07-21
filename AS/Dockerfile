# Specify the base image to use
# python:3.11-slim is a lightweight base image that contains Python 3.11 and a minimal set of tools
FROM python:3.11-slim

# Set environment variable to show real-time logs
ENV PYTHONUNBUFFERED=1

# Navigate to the working directory inside the container
# app directory will be created inside the container if it doesn't exist
WORKDIR /app

# Copy local files to a directory inside the container
COPY . .

# Expose UDP port
EXPOSE 53533/udp

# Specify the command to be executed when the container starts
# In our case, we want to run the app.py file
CMD ["python", "app.py"]