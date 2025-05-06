SaaS de Pedidos con Suscripción y Entregas – Backend Auth
Este proyecto es una API backend desarrollada con Django que proporciona autenticación personalizada para un sistema SaaS de pedidos con suscripción y entregas. Incluye endpoints para registro y login de usuarios, utilizando tokens JWT para la autenticación.

Características
Registro de usuarios con validación de contraseña.

Autenticación JWT para sesiones seguras.

Endpoints RESTful para operaciones de autenticación.

Pruebas automatizadas para garantizar la funcionalidad del sistema.

Docker para facilitar la implementación y el despliegue.

Requisitos Previos
Python 3.8 o superior

Docker y Docker Compose (opcional, para contenedores)

pipenv o virtualenv para gestión de entornos virtuales

Instalación y Ejecución
Clona el repositorio:

git clone https://github.com/Samuels2018/SaaS_de_pedidos_con_suscripci-n_y_entregas_concepto_auth.git
cd SaaS_de_pedidos_con_suscripci-n_y_entregas_concepto_auth
Crea y activa un entorno virtual:

python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
Instala las dependencias:

pip install -r requirements.txt
Configura las variables de entorno:

Copia el archivo .env.example y renómbralo a .env. Luego, ajusta las variables según tu configuración.

Ejecuta las migraciones:

python manage.py migrate
Inicia el servidor de desarrollo:

python manage.py runserver
El servidor estará disponible en http://127.0.0.1:8000/.



# ejecucion de los test
python manage.py test custom_auth.tests


# endpoints

post
http://127.0.0.1:8000/api/register/

{
  "email": "s@gmail.com",
  "password": "12345",
  "username": "sam11",
  "first_name": "sam",
  "last_name": "medina",
  "re_password": "12345"
}

respuesta esperada 
{
  "message": "Usuario registrado con éxito"
}

post
http://127.0.0.1:8000/api/login/  

{
  "email": "s@gmail.com",
  "password": "12345"
}

# respuesta esperada 

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3NDY0OTIwMTcsImlhdCI6MTc0NjQ4ODQxN30.loGOlB5egwjEvQYHhaKHGmXxsFq_xNzA1CDEoT-DKU8",
  "expires_at": "2025-05-06T11:40:17.987"
}


get
http://127.0.0.1:8000/api/profile/

with autorization
Authorization 
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3NDY0OTIwMTcsImlhdCI6MTc0NjQ4ODQxN30.loGOlB5egwjEvQYHhaKHGmXxsFq_xNzA1CDEoT-DKU8

respuesta esperada 

{
  "username": "sam11",
  "email": "s@gmail.com",
  "first_name": "sam",
  "last_name": "medina"
}

put 
http://127.0.0.1:8000/api/profile/

with autorization
Authorization 
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3NDY0OTIwMTcsImlhdCI6MTc0NjQ4ODQxN30.loGOlB5egwjEvQYHhaKHGmXxsFq_xNzA1CDEoT-DKU8

{
  "email": "s@gmail.com",
  "password": "12345",
  "username": "sam1111",
  "first_name": "sam",
  "last_name": "medina",
  "re_password": "12345"
}


respuesta esperada 
{
  "message": "Perfil actualizado con éxito"
}

delete
http://127.0.0.1:8000/api/profile/

with autorization
Authorization 
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3NDY0OTIwMTcsImlhdCI6MTc0NjQ4ODQxN30.loGOlB5egwjEvQYHhaKHGmXxsFq_xNzA1CDEoT-DKU8

respuesta esperada 
{
  "message": "Usuario eliminado con éxito"
}


Docker
Este proyecto incluye un run.sh para facilitar el despliegue del servicio con Docker.

Pasos para usar Docker:
Asegúrate de que Docker esté instalado.

Concede permisos de ejecución al script:

chmod +x run.sh
Ejecuta el script para construir y levantar el contenedor:

./run.sh
Esto construirá la imagen y levantará el contenedor en segundo plano. La API estará disponible en http://localhost:8000/