# Base image
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential

# Copy the proxy server script
COPY proxy_server.py /app/proxy_server.py

# Set the working directory
WORKDIR /app

# Expose the ports for master and workers
EXPOSE 6000
EXPOSE 6001-6010

# Set the entrypoint to run the proxy server
ENTRYPOINT ["python", "proxy_server.py"]
