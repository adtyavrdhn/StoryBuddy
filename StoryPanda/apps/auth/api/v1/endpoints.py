from ninja import Router
from ninja.security import django_auth
from ninja.throttling import UserRateThrottle
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from apps.users.models import User
from apps.users.api.v1 import schemas
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth

auth_router = Router()


@auth_router.post("/register")
def register(request, payload: schemas.UserIn):
    try:
        if User.objects.filter(email=payload.email).exists():
            return {"error": "Email already registered"}
        validate_password(payload.password)

        User.objects.create_user(
            username=payload.email, email=payload.email, password=payload.password
        )
        return {"success": "User registered successfully"}
    except Exception as e:
        return {"error": str(e)}


# JWT Login Endpoint
@auth_router.post("/login")
def login_view(request, payload: schemas.UserIn):
    user = authenticate(request, username=payload.email, password=payload.password)
    if user:
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
    return {"error": "Invalid credentials"}


# JWT Protected Route
@auth_router.get("/profile", auth=JWTAuth())
def user_profile(request):
    return {
        "username": request.user.username,
        "email": request.user.email,
    }


# Logout by Blacklisting Token (Optional)
@auth_router.post("/logout", auth=JWTAuth())
def logout_view(request):
    try:
        token = request.headers.get("Authorization").split()[1]
        RefreshToken(token).blacklist()
        return {"message": "Successfully logged out"}
    except Exception as e:
        return {"error": f"Logout Failed: {e}"}
