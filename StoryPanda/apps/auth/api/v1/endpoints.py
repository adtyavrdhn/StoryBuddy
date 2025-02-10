from ninja import Router
from ninja.security import django_auth
from ninja.throttling import UserRateThrottle
from django.contrib.auth.password_validation import validate_password
from ninja.errors import HttpError
from django.contrib.auth import authenticate
from apps.users.models import User
from apps.users.api.v1 import schemas
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth

auth_router = Router()


@auth_router.post("/register", throttle=[UserRateThrottle("10/h")])
def register(request, payload: schemas.UserIn):
    try:
        if User.objects.filter(email=payload.email).exists():
            raise HttpError(400, "Email already registered")
        validate_password(payload.password)

        User.objects.create_user(
            username=payload.email, email=payload.email, password=payload.password
        )
        return {"success": "User registered successfully"}
    except Exception as e:
        raise HttpError(500, f"Internal Server Error: {e}")


# JWT Login Endpoint
@auth_router.post("/login", throttle=[UserRateThrottle("10/h")])
def login_view(request, payload: schemas.UserIn):
    try:
        user = authenticate(request, username=payload.email, password=payload.password)
        if user:
            refresh = RefreshToken.for_user(user)
            return {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        else:
            raise HttpError(401, "Invalid email or password")

    except Exception as e:
        raise HttpError(500, "Internal Server Error")


# JWT Protected Routes
@auth_router.get("/profile", auth=JWTAuth())
def user_profile(request):
    return {
        "email": request.user.email,
    }


# Logout by Blacklisting Token (Optional)
@auth_router.post("/logout", auth=JWTAuth())
def logout_view(request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HttpError(400, "Authorization header missing or invalid")
        token = auth_header.split()[1]
        RefreshToken(token).blacklist()
        return {"message": "Successfully logged out"}
    except Exception as e:
        return {"error": f"Logout Failed: {e}"}
