FROM python:3-slim

# Update and install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential pkg-config\
    && pip install --no-cache-dir --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy and install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy code into container
COPY . .

EXPOSE 8080

# Run the application
CMD ["python", "server.py"]
