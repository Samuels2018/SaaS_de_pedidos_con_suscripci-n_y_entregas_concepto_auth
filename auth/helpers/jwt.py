import jwt
from datetime import datetime, timedelta
from django.conf import settings
from typing import Any

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'

def create_jwt_token (user_id, expired_in=3600) -> str:

  payload = {
    'user_id': user_id,
    'exp': datetime.utcnow() + timedelta(seconds=expired_in),
    'iat': datetime.utcnow()
  }

  token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
  return token


def decode_jwt_token (token) -> dict[str, Any] | None:
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
  except jwt.ExpiredSignatureError:
    return None
  except jwt.InvalidTokenError:
    return None
  

