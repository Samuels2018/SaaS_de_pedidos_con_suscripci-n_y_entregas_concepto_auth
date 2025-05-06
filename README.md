

# ejecucion de los test
python manage.py test auth.tests


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
