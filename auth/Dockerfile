FROM python:3-slim

# Update and install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential default-libmysqlclient-dev pkg-config\
    && pip install --no-cache-dir --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy and install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy code into container
COPY . .

EXPOSE 5000

# Run the application
CMD ["python", "server.py"]