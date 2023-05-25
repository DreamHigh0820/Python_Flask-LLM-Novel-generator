# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
WORKDIR /app
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Make port 8080 available to the world outside this container
EXPOSE 8080
# Run the command to start the server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]