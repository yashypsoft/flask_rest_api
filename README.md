# My REST API

## Overview

This is a simple REST API built with Flask, Dockerized, and ready for deployment on Kubernetes. It includes the following features:

- `/metrics` for Prometheus metrics
- `/health` for health checks
- `/v1/tools/lookup` to resolve IPv4 addresses for a domain
- `/v1/tools/validate` to validate IPv4 addresses
- `/v1/history` to retrieve the last 20 saved queries

## Setup

### Prerequisites

- Docker
- Docker Compose
- Python 3.9+
- MySQL

### Running the Application

1. Build and run the application using Docker Compose:

    ```bash
    docker-compose up -d --build
    ```

2. Initialize the database:

    ```bash
    docker-compose exec web flask db init
    docker-compose exec web flask db migrate -m "Initial migration."
    docker-compose exec web flask db upgrade
    ```

3. Access the API at `http://localhost:3000`.

## Kubernetes Deployment

### Using Helm

1. Customize the Helm chart.
2. Deploy to your Kubernetes cluster:

    ```bash
    helm install my-rest-api ./my_rest_api
    ```

## CI Pipeline

This repository includes a GitHub Actions CI pipeline that:

- Lints the code using `flake8`
- Builds and pushes a Docker image to Docker Hub

## API Documentation

### Lookup Domain

- **Endpoint:** `/v1/tools/lookup`
- **Method:** `GET`
- **Query Parameters:** `domain`

### Validate IP

- **Endpoint:** `/v1/tools/validate`
- **Method:** `POST`
- **Payload:**
  ```json
  {
    "ip": "192.168.0.1"
  }
