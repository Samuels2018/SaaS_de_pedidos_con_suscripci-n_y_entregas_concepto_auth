from django.test import TestCase, RequestFactory
from ..models import UserAccount
from ..views import RegisterUserView
import bcrypt
import json
from typing import Self


class RegisterUSerViewTestCase(TestCase):
  def setUp(self: Self) -> None:
    self.factory = RequestFactory()
    # datos simulados
    self.valid_data = {
      'username': 'testuser',
      'email': 'test@example.com',
      'password': 'securepassword123',
      're_password': 'securepassword123',
      'first_name': 'Test',
      'last_name': 'User'
    }

  # aserciones de un registo exitoso
  def test_success_registration (self: Self) -> None:
    request = self.factory.post('api/register/', data=json.dumps(self.valid_data), content_type='application/json')
    response = RegisterUserView().post(request)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(UserAccount.objects.count(), 1)

    user = UserAccount.objects.get(username=self.valid_data['username'])
    self.assertEqual(user.username, 'testuser')
    self.assertEqual(user.email, 'test@example.com')
    self.assertTrue(bcrypt.checkpw(
      self.valid_data['password'].encode('utf-8'), 
      user.password_hash.encode('utf-8')
    ))

  # asserciones para el caso de campos vacios
  def test_missing_required_fields (self: Self) -> None:
    test_case = [
      {'field': 'username', 'data': {**self.valid_data, 'username': ''}},
      {'field': 'email', 'data': {**self.valid_data, 'email': ''}},
      {'field': 'password', 'data': {**self.valid_data, 'password': ''}},
    ]

    for case in test_case:
      with self.subTest(field=case['field']):
        request = self.factory.post(
          'api/register/',
          data=json.dumps(case['data']),
          content_type='application/json'
        )

        response = RegisterUserView().post(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.content))
        self.assertEqual(UserAccount.objects.count(), 0)

  
  # caso de email duplicado
  def test_duplicate_email (self: Self) -> None:
    UserAccount.objects.create(
      username='existinguser',
      email='test@example.com',
      password_hash=bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    )

    request = self.factory.post(
      'api/register/',
      data=json.dumps(self.valid_data),
      content_type='application/json'
    )
    response = RegisterUserView().post(request)
    response_data = json.loads(response.content)
    
    self.assertEqual(response.status_code, 400)
    self.assertIn(response_data['error'], 'El correo electrónico ya está en uso')
    self.assertEqual(UserAccount.objects.count(), 1)


  def test_duplicate_username(self: Self) -> None:
    # Test que no se permiten usernames duplicados
    # Crear usuario primero
    UserAccount.objects.create(
      username='testuser',
      email='existing@example.com',
      password_hash=bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    )
    
    request = self.factory.post(
      'api/register/',
      data=json.dumps(self.valid_data),
      content_type='application/json'
    )
    response = RegisterUserView().post(request)
    response_data = json.loads(response.content)
    
    self.assertEqual(response.status_code, 400)
    self.assertIn(response_data['error'], 'El nombre de usuario ya está en uso')
    self.assertEqual(UserAccount.objects.count(), 1)

  def test_password_mismatch(self: Self) -> None:
    # Test que las contraseñas deben coincidir
    data = {
      **self.valid_data,
      're_password': 'differentpassword'
    }
    
    request = self.factory.post(
      'api/register/',
      data=json.dumps(data),
      content_type='application/json'
    )
    response = RegisterUserView().post(request)
    response_data = json.loads(response.content)
    
    self.assertEqual(response.status_code, 400)
    self.assertIn(response_data['error'], 'Las contraseñas no coinciden')
    self.assertEqual(UserAccount.objects.count(), 0)

  def test_password_hashing(self: Self) -> None:
    # Test que las contraseñas se hashean correctamente
    request = self.factory.post(
      'api/register/',
      data=json.dumps(self.valid_data),
      content_type='application/json'
    )

    RegisterUserView().post(request)
    
    user = UserAccount.objects.first()
    self.assertTrue(bcrypt.checkpw(
      self.valid_data['password'].encode('utf-8'),
      user.password_hash.encode('utf-8')
    ))
    self.assertNotEqual(user.password_hash, self.valid_data['password'])


  def test_invalid_content_type(self: Self) -> None:
    # Test que solo acepta application/json
    request = self.factory.post(
      'api/register/',
      data=self.valid_data,
      content_type='text/plain'
    )
    response = RegisterUserView().post(request)
    self.assertEqual(response.status_code, 400)

  def test_empty_json(self: Self):
    # Test con JSON vacío
    request = self.factory.post(
      '/register/',
      data=json.dumps({}),
      content_type='application/json'
    )
    response = RegisterUserView().post(request)
    self.assertEqual(response.status_code, 400)


