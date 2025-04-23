from django.test import TestCase, RequestFactory
from models import UserAccount, AuthToken
from ..helpers import create_jwt_token
from ..views import UserProfileView
import json
from typing import Self
import bcrypt
from django.utils import timezone
from datetime import timedelta

class UserProfileViewTest (TestCase):
  def setUp(self):
    self.factory = RequestFactory()
    # Crear un usuario de prueba
    self.test_password = 'testpassword123'
    self.hashed_password = bcrypt.hashpw(self.test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    self.user = UserAccount.objects.create(
      email='test@example.com',
      username='testuser',
      password_hash=self.hashed_password,
      first_name='Test',
      last_name='User'
    )
    
    # Crear un token válido
    self.valid_token = create_jwt_token(self.user.id)
    AuthToken.objects.create(
      user=self.user,
      token=self.valid_token,
      expires_at=timezone.now() + timedelta(hours=1)
    )
    
    # Datos válidos para actualización
    self.valid_update_data = {
      'username': 'updateduser',
      'email': 'updated@example.com',
      'first_name': 'Updated',
      'last_name': 'Name',
      'password': 'newpassword123'
    }


  def test_get_profile_success (self: Self) -> None:
    headers = {'Authorization': f'Bearer {self.valid_token}'}
    request = self.factory.post(
      '/profile/',
      content_type='application/json',
      **headers
    )

    response = UserProfileView().get(request)
    self.assertEqual(response.status_code, 200)
    response_data = json.loads(response.content)
    
    self.assertEqual(response_data['username'], 'testuser')
    self.assertEqual(response_data['email'], 'test@example.com')
    self.assertEqual(response_data['first_name'], 'Test')
    self.assertEqual(response_data['last_name'], 'User')

  def test_get_profile_missing_token(self: Self) -> None:
    """Test obtener perfil sin token"""
    request = self.factory.get(
      '/profile/',
      content_type='application/json'
    )
    response = UserProfileView().get(request)
    
    self.assertEqual(response.status_code, 401)
    self.assertIn('Token no proporcionado', str(response.content))

  def test_get_profile_invalid_token(self: Self) -> None:
    """Test obtener perfil con token inválido"""
    headers = {'Authorization': 'Bearer invalidtoken'}
    request = self.factory.get(
        '/profile/',
        content_type='application/json',
        **headers
    )
    response = UserProfileView().get(request)
    
    self.assertEqual(response.status_code, 401)
    self.assertIn('Token inválido o expirado', str(response.content))

  def test_get_profile_expired_token(self: Self) -> None:
    """Test obtener perfil con token expirado"""
    # Crear token expirado
    expired_token = create_jwt_token(self.user.id, expires_in=-3600)
    headers = {'Authorization': f'Bearer {expired_token}'}
    request = self.factory.get(
        '/profile/',
        content_type='application/json',
        **headers
    )
    response = UserProfileView().get(request)
    
    self.assertEqual(response.status_code, 401)
    self.assertIn('Token inválido o expirado', str(response.content))


  def test_update_profile_success(self: Self) -> None:
    """Test actualizar perfil con datos válidos"""
    headers = {'Authorization': f'Bearer {self.valid_token}'}
    request = self.factory.put(
      '/profile/',
      data=json.dumps(self.valid_update_data),
      content_type='application/json',
      **headers
    )
    response = UserProfileView().put(request)
    
    self.assertEqual(response.status_code, 200)
    self.assertIn('Perfil actualizado con éxito', str(response.content))
    
    # Verificar cambios en la base de datos
    updated_user = UserAccount.objects.get(id=self.user.id)
    self.assertEqual(updated_user.username, 'updateduser')
    self.assertEqual(updated_user.email, 'updated@example.com')
    self.assertEqual(updated_user.first_name, 'Updated')
    self.assertEqual(updated_user.last_name, 'Name')
    self.assertTrue(updated_user.check_password('newpassword123'))

  def test_update_profile_partial_data(self: Self) -> None:
    """Test actualizar solo algunos campos"""
    partial_data = {
      'first_name': 'Partial',
      'last_name': 'Update'
    }
    headers = {'Authorization': f'Bearer {self.valid_token}'}
    request = self.factory.put(
      '/profile/',
      data=json.dumps(partial_data),
      content_type='application/json',
      **headers
    )
    response = UserProfileView().put(request)
    
    self.assertEqual(response.status_code, 200)
    
    # Verificar cambios en la base de datos
    updated_user = UserAccount.objects.get(id=self.user.id)
    self.assertEqual(updated_user.first_name, 'Partial')
    self.assertEqual(updated_user.last_name, 'Update')
    # Campos no enviados deben permanecer igual
    self.assertEqual(updated_user.username, 'testuser')
    self.assertEqual(updated_user.email, 'test@example.com')

  def test_update_profile_duplicate_email(self: Self) -> None:
    """Test no permitir email duplicado"""
    # Crear otro usuario
    UserAccount.objects.create(
      email='existing@example.com',
      username='otheruser',
      password_hash=self.hashed_password
    )
    
    update_data = {'email': 'existing@example.com'}
    headers = {'Authorization': f'Bearer {self.valid_token}'}
    request = self.factory.put(
      '/profile/',
      data=json.dumps(update_data),
      content_type='application/json',
      **headers
    )
    response = UserProfileView().put(request)
    
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', json.loads(response.content))

  def test_update_profile_duplicate_username(self: Self) -> None:
    """Test no permitir username duplicado"""
    # Crear otro usuario
    UserAccount.objects.create(
      email='other@example.com',
      username='existinguser',
      password_hash=self.hashed_password
    )
    
    update_data = {'username': 'existinguser'}
    headers = {'Authorization': f'Bearer {self.valid_token}'}
    request = self.factory.put(
      '/profile/',
      data=json.dumps(update_data),
      content_type='application/json',
      **headers
    )
    response = UserProfileView().put(request)
    
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', json.loads(response.content))

  def test_update_profile_invalid_data(self: Self) -> None:
    """Test con datos de actualización inválidos"""
    invalid_data = {
      'email': 'notanemail',
      'password': 'short'
    }
    headers = {'Authorization': f'Bearer {self.valid_token}'}
    request = self.factory.put(
      '/profile/',
      data=json.dumps(invalid_data),
      content_type='application/json',
      **headers
    )
    response = UserProfileView().put(request)
    
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', json.loads(response.content))


  def test_delete_profile_success(self: Self) -> None:
    """Test eliminar cuenta de usuario"""
    headers = {'Authorization': f'Bearer {self.valid_token}'}
    request = self.factory.delete(
      '/profile/',
      content_type='application/json',
      **headers
    )
    response = UserProfileView().delete(request)
    
    self.assertEqual(response.status_code, 200)
    self.assertIn('Usuario eliminado con éxito', str(response.content))
    self.assertFalse(UserAccount.objects.filter(id=self.user.id).exists())
    self.assertFalse(AuthToken.objects.filter(user=self.user).exists())

  def test_delete_profile_missing_token(self: Self) -> None:
    """Test eliminar cuenta sin token"""
    request = self.factory.delete(
        '/profile/',
        content_type='application/json'
    )
    response = UserProfileView().delete(request)
    
    self.assertEqual(response.status_code, 401)
    self.assertIn('Token no proporcionado', str(response.content))
    self.assertTrue(UserAccount.objects.filter(id=self.user.id).exists())

  def test_delete_profile_invalid_token(self: Self) -> None:
    """Test eliminar cuenta con token inválido"""
    headers = {'Authorization': 'Bearer invalidtoken'}
    request = self.factory.delete(
        '/profile/',
        content_type='application/json',
        **headers
    )
    response = UserProfileView().delete(request)
    
    self.assertEqual(response.status_code, 401)
    self.assertIn('Token inválido o expirado', str(response.content))
    self.assertTrue(UserAccount.objects.filter(id=self.user.id).exists())

  def test_invalid_http_method(self: Self) -> None:
    """Test método HTTP no permitido (ej: POST)"""
    headers = {'Authorization': f'Bearer {self.valid_token}'}
    request = self.factory.post(
      '/profile/',
      content_type='application/json',
      **headers
    )
    response = UserProfileView().post(request)  # No implementado
    self.assertEqual(response.status_code, 405)  # Method Not Allowed