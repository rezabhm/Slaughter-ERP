# Docker-based Service Launcher

This directory contains the necessary files to build and run a Docker container that sequentially launches all the services defined in `services.yml`.

## Overview

The `Dockerfile` creates a container that uses a `launcher.sh` script to start each service one by one. The script performs the following steps for each service:

1.  Installs Python dependencies from `requirements.txt`.
2.  Generates a `.env` file using `init_env.py`.
3.  Runs `makemigrations` for the apps specified in `services.yml`.
4.  Applies database migrations using `migrate`.
5.  Starts the service on its configured port.
6.  Performs a health check to ensure the service is running before starting the next one.

## Prerequisites

- Docker must be installed on your system.

## Building the Image

To build the Docker image, run the following command from the project root:

```bash
docker build -t project-launcher -f docker/Dockerfile .
```

## Running the Container

To run the container, use the following command:

```bash
docker run --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 -p 8003:8003 -p 8004:8004 -p 8005:8005 project-launcher
```

This command maps the ports of the services running inside the container to the host machine.

### Overriding Environment Variables

You can override the environment variables used to generate the `.env` files by passing them to the `docker run` command. For example, to change the database host for all services, you can run:

```bash
docker run --rm -e DB_HOST=my-postgres-instance -p 8000:8000 -p 8001:8001 -p 8002:8002 -p 8003:8003 -p 8004:8004 -p 8005:8005 project-launcher
```

## Configuration

The `services.yml` file in the project root is used to configure which services are launched. You can add, remove, or modify services in this file.

### `services.yml` structure

```yaml
- name: <service_name>
  path: <path_to_service_directory>
  port: <port_number>
  apps:
    - <app1_name>
    - <app2_name>
  healthcheck_path: <healthcheck_endpoint>
```

- `name`: The name of the service.
- `path`: The path to the service's directory from the project root.
- `port`: The port on which the service will run.
- `apps`: A list of Django apps for which to run `makemigrations`.
- `healthcheck_path`: The path to the health check endpoint (e.g., `/healthz/`).
```
