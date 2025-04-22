from rest_framework import serializers
from .models import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserAccount
    fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password_hash']
    extra_kwargs = {'password_hash': {'write_only': True}}