#!/bin/bash

IMAGE_NAME="saas_auth"
CONTAINER_NAME="saas_auth_container"

PORT=8000

# Construir la imagen Docker
echo "Construyendo la imagen Docker..."
docker build -t $IMAGE_NAME .

# Verificar si la construcción fue exitosa
if [ $? -ne 0 ]; then
  echo "Error al construir la imagen Docker."
  exit 1
fi

# Ejecutar el contenedor
echo "Ejecutando el contenedor Docker..."
docker run -d -v $(pwd):/usr/src/app -p $PORT:8000 --name $CONTAINER_NAME $IMAGE_NAME


# Verificar si el contenedor se ejecutó correctamente
if [ $? -ne 0 ]; then
  echo "Error al ejecutar el contenedor Docker."
  exit 1
fi

echo "El contenedor está corriendo en el puerto $PORT."