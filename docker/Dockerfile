FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl libyaml-dev gcc && rm -rf /var/lib/apt/lists/*
RUN pip install pyyaml

# Copy the entire project context
COPY . /app/

# Copy the launcher script and services configuration
COPY services.yml /app/services.yml
COPY docker/launcher.sh /app/launcher.sh

# Make the launcher script executable
RUN chmod +x /app/launcher.sh

# Set the entrypoint
CMD ["/app/launcher.sh"]
