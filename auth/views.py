from django.views import View
from django.http.response import JsonResponse
from .models import UserAccount, AuthToken
from .helpers import create_jwt_token, decode_jwt_token, get_http_status_message
from datetime import datetime, timedelta 
# Create your views here.

class RegisterUserView(View):
  def post(self, request):
    data = request.data.json()
    if 'username' in data and 'password' in data:
      # Handle login
      pass
    elif 'email' in data and 'password' in data:
      # Handle registration
      pass

class LoginUserView(View):
  def post(self, request) -> JsonResponse:
    email = request.data.get('email')
    password = request.data.get('password')

    try:
      user = UserAccount.objects.get(email=email)
    except UserAccount.DoesNotExist:
      return JsonResponse({"error": "Usuario no encontrado"}, status=get_http_status_message(404))

    if not user.check_password(password):
      return JsonResponse({"error": "Contraseña incorrecta"}, status=get_http_status_message(401))

    # Genera un nuevo token JWT y lo guarda en la base de datos
    token = create_jwt_token(user.id)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    AuthToken.objects.create(user=user, token=token, expires_at=expires_at)

    return JsonResponse({
      "access_token": token,
      "expires_at": expires_at,
    })


class UserProfileView(View):
  def get(self, request) -> JsonResponse:
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
      return JsonResponse({"error": "Token no proporcionado"}, status=get_http_status_message(401))

    token = auth_header.split(' ')[1]
    payload = decode_jwt_token(token)
    if not payload:
      return JsonResponse({"error": "Token inválido o expirado"}, status=get_http_status_message(401))

    try:
      user = UserAccount.objects.get(id=payload['user_id'])
      return JsonResponse({
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
      })
    except UserAccount.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=get_http_status_message(404))

  def put(self, request):
    data = request.data.json()
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
      return JsonResponse({"error": "Token no proporcionado"}, status=get_http_status_message(401))
    token = auth_header.split(' ')[1]
    payload = decode_jwt_token(token)
    if not payload:
      return JsonResponse({"error": "Token inválido o expirado"}, status=get_http_status_message(401))
    try:
      user = UserAccount.objects.get(id=payload['user_id'])
      if 'username' in data:
        user.username = data['username']
      if 'email' in data:
        user.email = data['email']
      if 'first_name' in data:
        user.first_name = data['first_name']
      if 'last_name' in data:
        user.last_name = data['last_name']
      if 'password' in data:
        user.set_password(data['password'])
      user.save()
      return JsonResponse({"message": "Perfil actualizado con éxito"})
    except UserAccount.DoesNotExist:
      return JsonResponse({"error": "Usuario no encontrado"}, status=get_http_status_message(404))
    

  def delete(self, request):
    data = request.data.json()
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
      return JsonResponse({"error": "Token no proporcionado"}, status=get_http_status_message(401))
    token = auth_header.split(' ')[1]
    payload = decode_jwt_token(token)
    if not payload:
      return JsonResponse({"error": "Token inválido o expirado"}, status=get_http_status_message(401))
    try:
      user = UserAccount.objects.get(id=payload['user_id'])
      user.delete()
      return JsonResponse({"message": "Usuario eliminado con éxito"})
    except UserAccount.DoesNotExist:
      return JsonResponse({"error": "Usuario no encontrado"}, status=get_http_status_message(404))

        
