# lets_hack

Quick start: run with Docker Compose (Windows PowerShell)
- Prerequisites: Ensure an env file exists for your profile (e.g., dev.env). You can copy dev.env.example to dev.env and adjust values.
- From the repo root, run the following in PowerShell:

  1) Set required variables for this session:
     - $env:ENV = 'dev'
     - $env:IP_ADDR = 'YOUR_REGISTRY_HOST_OR_IP'
     - $env:DOCKER_IMAGE_VERSION = 'latest'

  2) Start services:
     docker compose -f .\docker-compose-persist.yml up -d

  3) Stop services:
     docker compose -f .\docker-compose-persist.yml down

- Exposed ports:
  - API: http://localhost:8000
  - Postgres: localhost:5436