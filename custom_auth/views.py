from django.views import View
from django.http.response import JsonResponse
from .models import UserAccount, AuthToken
from .helpers import create_jwt_token, decode_jwt_token, get_http_status_message
from datetime import datetime, timedelta 
import bcrypt
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import uuid
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(View):
  def post(self, request) -> JsonResponse:
    if request.content_type != 'application/json':
      return JsonResponse({"error": "El tipo de contenido debe ser application/json"}, status=400)
    
    print("RegisterUserView")
    print(json.loads(request.body))
    data=json.loads(request.body)
    if not data.get('username') or not data.get('email') or not data.get('password'):
      return JsonResponse({"error": "Faltan datos obligatorios"}, status=400)
    if UserAccount.objects.filter(email=data.get('email')).exists():
      return JsonResponse({"error": "El correo electrónico ya está en uso"}, status=400)
    if UserAccount.objects.filter(username=data.get('username')).exists():
      return JsonResponse({"error": "El nombre de usuario ya está en uso"}, status=400)
    
    hash_password = bcrypt.hashpw(data.get('password', '').encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    print(hash_password)
    
    if data.get('password') != data.get('re_password'):
      return JsonResponse({"error": "Las contraseñas no coinciden"}, status=400)
    
    print(hash_password)
    
    user = UserAccount(
      user_id=str(uuid.uuid4()),
      username=data.get('username'),
      email=data.get('email'),
      password_hash=hash_password,
      first_name=data.get('first_name'),
      last_name=data.get('last_name')
    )
    user.save()
    return JsonResponse({"message": "Usuario registrado con éxito"}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class LoginUserView(View):
  def post(self, request) -> JsonResponse:
    if request.content_type != 'application/json':
      return JsonResponse({"error": "El tipo de contenido debe ser application/json"}, status=400)
    
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
      return JsonResponse({"error": "Faltan datos obligatorios"}, status=400)

    try:
      user = UserAccount.objects.get(email=email)
    except UserAccount.DoesNotExist:
      return JsonResponse({"error": "Usuario no encontrado"}, status=404)
    

    # Verifica la contraseña
    if not (bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))):
      print("Contraseña incorrecta")
      return JsonResponse({"error": "Contraseña incorrecta"},  status=401)
      
    # Genera un nuevo token JWT y lo guarda en la base de datos
    token = create_jwt_token(user.id)
    expires_at = datetime.utcnow() + timedelta(hours=12)
    AuthToken.objects.create(user=user, token=token, expires_at=expires_at)

    return JsonResponse({
      "access_token": token,
      "expires_at": (expires_at).strftime("%Y-%m-%d %H:%M:%S"),
    }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(View):
  def get(self, request) -> JsonResponse:
    if request.content_type != 'application/json':
      return JsonResponse({"error": "El tipo de contenido debe ser application/json"}, status=400)
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
      return JsonResponse({"error": "Token no proporcionado"}, status=401)

    token = auth_header.split(' ')[1]
    payload = decode_jwt_token(token)
    if not payload:
      return JsonResponse({"error": "Token inválido o expirado"}, status=401)

    try:
      user = UserAccount.objects.get(id=payload['user_id'])
      return JsonResponse({
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
      }, status=200)
    except UserAccount.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)

  def put(self, request) -> JsonResponse:
    if request.content_type != 'application/json':
      return JsonResponse({"error": "El tipo de contenido debe ser application/json"}, status=400)
    
    data = json.loads(request.body)
    auth_header = request.headers.get('Authorization')
    hash_password = None
    if not auth_header or not auth_header.startswith('Bearer '):
      return JsonResponse({"error": "Token no proporcionado"}, status=401)
    token = auth_header.split(' ')[1]
    payload = decode_jwt_token(token)
    if not payload:
      return JsonResponse({"error": "Token inválido o expirado"}, status=401)
    try:
      user = UserAccount.objects.get(id=payload['user_id'])
      if 'username' in data:
        if UserAccount.objects.filter(username=data.get('username')).exclude(id=user.id).exists():
          return JsonResponse({'error': 'Username already in use'}, status=400)
        user.username = data.get('username')
      if 'email' in data:
        if UserAccount.objects.filter(email=data['email']).exclude(id=user.id).exists():
          return JsonResponse({'error': 'Email already in use'}, status=400)
        user.email = data.get('email')
      if 'first_name' in data:
        user.first_name = data.get('first_name', '')
      if 'last_name' in data:
        user.last_name = data.get('last_name', '')
      if 'password' in data:
        if not (bcrypt.checkpw(data.get('password').encode('utf-8'), user.password_hash.encode('utf-8'))):
          if data.get('password') != data.get('re_password'):
            return JsonResponse({"error": "Las contraseñas no coinciden"}, status=400)
          hash_password = bcrypt.hashpw(data.get('password', '').encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

          user.password_hash = hash_password
      user.save()
      return JsonResponse({"message": "Perfil actualizado con éxito"}, status=200)
    except UserAccount.DoesNotExist:
      return JsonResponse({"error": "Usuario no encontrado"}, status=404)
    

  def delete(self, request) -> JsonResponse:
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
      return JsonResponse({"error": "Token no proporcionado"}, status=401)
    token = auth_header.split(' ')[1]
    payload = decode_jwt_token(token)
    if not payload:
      return JsonResponse({"error": "Token inválido o expirado"}, status=401)
    try:
      user = UserAccount.objects.get(id=payload['user_id'])
      user.delete()
      return JsonResponse({"message": "Usuario eliminado con éxito"})
    except UserAccount.DoesNotExist:
      return JsonResponse({"error": "Usuario no encontrado"}, status=404)
    
  def http_method_not_allowed(self, request, *args, **kwargs):
    return JsonResponse({"error": "Método no permitido"}, status=405)

        
