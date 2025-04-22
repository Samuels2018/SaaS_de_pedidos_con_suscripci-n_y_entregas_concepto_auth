from django.db import models
import uuid

# Create your models here.

class UserAccount(models.Model):
  id = models.AutoField(primary_key=True)
  user_id = models.CharField(max_length=255, unique=True)
  email = models.EmailField(unique=True)
  username = models.CharField(max_length=150, unique=True)
  password_hash = models.CharField(max_length=128)
  first_name = models.CharField(max_length=30, blank=True)
  last_name = models.CharField(max_length=30, blank=True)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.username
  
class AuthToken(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='tokens')
  token = models.CharField(max_length=500, unique=True)
  expires_at = models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Token for {self.user.username}"
