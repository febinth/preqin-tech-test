# preqin-tech-test

This repository contains two apps, preqin-api and a Django app, each in their own directory. The Django application calls the preqin-api (https://github.com/JayGadi/preqin-technical-test) to fetch investor and commitments data.

The preqin-api is added as a git submodule to this repo. Both apps can be managed and orchestrated using Docker Compose.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the App

1. Clone the repository:
   ```sh
   git clone --recurse-submodules https://github.com/febinth/preqin-tech-test
   cd preqin-tech-test
   git submodule update --init --recursive
2. Use docker compose to bring up both the apps.
   ```sh
   cd preqin-tech-test
   docker-compose -f docker-compose.yaml up -d
3. Run the django app from `localhost:8000/preqin/investors/`
   

