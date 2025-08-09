#!/bin/bash

set -e

# Function to extract values from YAML
# Note: This is a very basic YAML parser. It will work for the structure of services.yml, but it's not a general-purpose parser.
# It relies on the fact that the keys are unique and the structure is consistent.
get_yaml_value() {
    python3 -c "import yaml;import sys;data=yaml.safe_load(open(sys.argv[1]));print(data[$2]['$3'])" "$1" "$4" "$5"
}

get_yaml_list() {
    python3 -c "import yaml;import sys;data=yaml.safe_load(open(sys.argv[1]));print(' '.join(data[$2]['$3']))" "$1" "$4" "$5"
}

# Read the services.yml file
SERVICES_FILE="services.yml"
SERVICES_COUNT=$(python3 -c "import yaml;import sys;data=yaml.safe_load(open(sys.argv[1]));print(len(data))" "$SERVICES_FILE")

echo "Found $SERVICES_COUNT services to launch."

# Loop through each service
for i in $(seq 0 $(($SERVICES_COUNT - 1))); do
    NAME=$(get_yaml_value "$SERVICES_FILE" "$i" "name")
    PATH_DIR=$(get_yaml_value "$SERVICES_FILE" "$i" "path")
    PORT=$(get_yaml_value "$SERVICES_FILE" "$i" "port")
    HEALTHCHECK_PATH=$(get_yaml_value "$SERVICES_FILE" "$i" "healthcheck_path")
    APPS=$(get_yaml_list "$SERVICES_FILE" "$i" "apps")

    echo "========================================================================================================"
    echo "Starting service: $NAME"
    echo "========================================================================================================"

    # Navigate to the service directory
    cd "$PATH_DIR"

    # Install dependencies
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt

    # Generate .env file
    echo "Generating .env file..."
    python auto_init_env.py

    # Run makemigrations
    echo "Running makemigrations for apps: $APPS..."
    python manage.py makemigrations $APPS

    # Run migrate
    echo "Running migrate..."
    python manage.py migrate --noinput

    # Start the service in the background
    echo "Starting $NAME on port $PORT..."
    gunicorn configs.wsgi:application --bind 0.0.0.0:"$PORT" &

    # Health check
    echo "Waiting for $NAME to be healthy..."
    while true; do
        if curl -f "http://127.0.0.1:$PORT$HEALTHCHECK_PATH"; then
            echo "$NAME is healthy."
            break
        fi
        echo "Waiting for $NAME..."
        sleep 5
    done

    # Go back to the root directory
    cd -
done

echo "All services are up and running."

# Wait for all background processes to finish
wait
