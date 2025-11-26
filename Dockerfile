# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the source code (todo_cli.py) into the container at /app
# Note: For simplicity, copy only the necessary production code.
COPY src/main/python/todo_cli.py /app/

# The application is designed to be run interactively, 
# but for the purpose of a Docker image, we set the entrypoint.
CMD ["python", "todo_cli.py"]
