#!/bin/bash

# Build the Docker image
docker build -t saas_auth .

# Run the Docker container with volume mapping
docker run --rm -it \
  -v $(pwd):/usr/src/app \  # Mapea el directorio actual al contenedor
  -p 8000:8000 \            # Expone el puerto 8000
  saas_auth