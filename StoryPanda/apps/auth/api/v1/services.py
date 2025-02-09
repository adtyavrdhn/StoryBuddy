# apps/users/auth.py
from datetime import datetime, timedelta
from typing import Optional
from ninja.security import HttpBearer
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            return user
        except (jwt.PyJWTError, User.DoesNotExist):
            return None


def create_token(user_id: int) -> dict:
    """Create access and refresh tokens for the user"""
    access_payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=60),  # 1 hour
        "type": "access",
    }

    refresh_payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7),  # 7 days
        "type": "refresh",
    }

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

    return {"access_token": access_token, "refresh_token": refresh_token}
