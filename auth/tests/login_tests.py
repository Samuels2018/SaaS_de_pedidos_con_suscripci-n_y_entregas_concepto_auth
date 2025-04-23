from django.test import TestCase, RequestFactory
from models import UserAccount, AuthToken
from ..views import LoginUserView
import json
from typing import Self
import bcrypt
from django.utils import timezone
from datetime import timedelta, datetime

class LoginUserViewTestCase(TestCase):
  def setUp(self: Self) -> None:
    self.factory = RequestFactory()
    self.test_password = 'testpassword123'
    self.hashed_password = bcrypt.hashpw(self.test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    self.user = UserAccount.objects.create(
      email='test@example.com',
      username='testuser',
      password_hash=self.hashed_password,
      first_name='Test',
      last_name='User'
    )
    self.valid_data = {
      'email': 'test@example.com',
      'password': 'testpassword123'
    }

  def test_successful_login(self: Self) -> None:
    request = self.factory.post(
      '/login/',
      data=json.dumps(self.valid_data),
      content_type='application/json'
    )
    response = LoginUserView().post(request)
    self.assertEqual(response.status_code, 200)
    response_data = json.loads(response.content)

    self.assertIn('access_token', response_data)
    self.assertIn('expires_at', response_data)

    # Verificar que se creó un token en la base de datos
    self.assertEqual(AuthToken.objects.count(), 1)
    auth_token = AuthToken.objects.first()
    self.assertEqual(auth_token.user, self.user)
    self.assertEqual(auth_token.token, response_data['access_token'])
    
    # Verificar la fecha de expiración (aproximadamente)
    expires_at = datetime.strptime(response_data['expires_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    expected_expiry = timezone.now() + timedelta(hours=1)
    self.assertAlmostEqual(
      expires_at.timestamp(),
      expected_expiry.timestamp(),
      delta=5  # Margen de 5 segundos
    )

  def test_invalid_password(self: Self) -> None:
    invalid_data = {
      'email': 'test@example.com',
      'password': 'wrongpassword'
    }
        
    request = self.factory.post(
      '/login/',
      data=json.dumps(invalid_data),
      content_type='application/json'
    )
    response = LoginUserView().post(request)
    
    self.assertEqual(response.status_code, 401)
    self.assertIn('Contraseña incorrecta', str(response.content))
    self.assertEqual(AuthToken.objects.count(), 0)

  def test_nonexistent_email(self: Self):
    """Test que email no registrado devuelve error"""
    invalid_data = {
      'email': 'nonexistent@example.com',
      'password': 'anypassword'
    }
    
    request = self.factory.post(
      '/login/',
      data=json.dumps(invalid_data),
      content_type='application/json'
    )
    response = LoginUserView().post(request)
    
    self.assertEqual(response.status_code, 404)
    self.assertIn('Usuario no encontrado', str(response.content))
    self.assertEqual(AuthToken.objects.count(), 0)


  def test_missing_email(self: Self):
    """Test que falta el campo email"""
    invalid_data = {
      'password': 'testpassword123'
    }
    
    request = self.factory.post(
      '/login/',
      data=json.dumps(invalid_data),
      content_type='application/json'
    )
    response = LoginUserView().post(request)
    
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', json.loads(response.content))
    self.assertEqual(AuthToken.objects.count(), 0)

  def test_missing_password(self: Self):
    """Test que falta el campo password"""
    invalid_data = {
      'email': 'test@example.com'
    }
    
    request = self.factory.post(
      '/login/',
      data=json.dumps(invalid_data),
      content_type='application/json'
    )
    response = LoginUserView().post(request)
    
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', json.loads(response.content))
    self.assertEqual(AuthToken.objects.count(), 0)

  def test_empty_credentials(self: Self):
    """Test con credenciales vacías"""
    invalid_data = {
      'email': '',
      'password': ''
    }
    
    request = self.factory.post(
      '/login/',
      data=json.dumps(invalid_data),
      content_type='application/json'
    )
    response = LoginUserView().post(request)
    
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', json.loads(response.content))
    self.assertEqual(AuthToken.objects.count(), 0)

  def test_response_format(self: Self):
    """Test que la respuesta tiene el formato correcto"""
    request = self.factory.post(
      '/login/',
      data=json.dumps(self.valid_data),
      content_type='application/json'
    )
    response = LoginUserView().post(request)
    
    response_data = json.loads(response.content)
    self.assertIn('access_token', response_data)
    self.assertIn('expires_at', response_data)
    
    # Verificar que el token es un string no vacío
    self.assertIsInstance(response_data['access_token'], str)
    self.assertGreater(len(response_data['access_token']), 10)
    
    # Verificar que expires_at es una fecha válida
    try:
      datetime.strptime(response_data['expires_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
      self.fail("expires_at no tiene un formato de fecha válido")


  def test_multiple_logins_create_multiple_tokens(self: Self):
    """Test que múltiples logins crean múltiples tokens válidos"""
    # Primer login
    request1 = self.factory.post(
      '/login/',
      data=json.dumps(self.valid_data),
      content_type='application/json'
    )
    response1 = LoginUserView().post(request1)
    token1 = json.loads(response1.content)['access_token']
    
    # Segundo login
    request2 = self.factory.post(
      '/login/',
      data=json.dumps(self.valid_data),
      content_type='application/json'
    )
    response2 = LoginUserView().post(request2)
    token2 = json.loads(response2.content)['access_token']
    
    # Verificar que son tokens diferentes
    self.assertNotEqual(token1, token2)
    
    # Verificar que ambos tokens están en la base de datos
    self.assertEqual(AuthToken.objects.count(), 2)
    self.assertTrue(AuthToken.objects.filter(token=token1).exists())
    self.assertTrue(AuthToken.objects.filter(token=token2).exists())


  def test_invalid_content_type(self: Self):
    """Test que solo acepta application/json"""
    request = self.factory.post(
      '/login/',
      data=self.valid_data,
      content_type='text/plain'
    )
    response = LoginUserView().post(request)
    self.assertEqual(response.status_code, 400)

  def test_inactive_user(self: Self):
    """Test que un usuario inactivo no puede iniciar sesión"""
    # Crear usuario inactivo
    UserAccount.objects.create(
      email='inactive@example.com',
      username='inactive',
      password_hash=self.hashed_password,
      is_active=False
    )
    
    request = self.factory.post(
      '/login/',
      data=json.dumps({
        'email': 'inactive@example.com',
        'password': 'testpassword123'
      }),
      content_type='application/json'
    )
    response = LoginUserView().post(request)
    
    self.assertEqual(response.status_code, 403)
    self.assertIn('error', json.loads(response.content))
    self.assertEqual(AuthToken.objects.count(), 0)