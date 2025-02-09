# # apps/users/api/v1/endpoints.py
# from ninja import Router
# from django.contrib.auth import authenticate
# from apps.users.auth import create_token, AuthBearer
# from .schemas import AuthLoginSchema, AuthOut, RefreshSchema, TokenSchema
# import jwt
# from django.conf import settings
# from apps.users.api.v1.schemas import UserOut


#


# @auth_router.post("/login", response=AuthOut)
# def login(request, payload: AuthLoginSchema):
#     user = authenticate(email=payload.email, password=payload.password)
#     if not user:
#         return {"message": "Invalid credentials", "token": None}, 401

#     token = create_token(user.id)
#     return {"message": "Login successful", "token": token}


# @auth_router.post("/refresh", response=TokenSchema)
# def refresh_token(request, payload: RefreshSchema):
#     try:
#         payload = jwt.decode(
#             payload.refresh_token, settings.SECRET_KEY, algorithms=["HS256"]
#         )
#         if payload["type"] != "refresh":
#             return {"message": "Invalid token type"}, 401

#         token = create_token(payload["user_id"])
#         return token
#     except jwt.PyJWTError:
#         return {"message": "Invalid token"}, 401


# # Protected route example
# @protected_router.get("/me", response=UserOut)
# def get_me(request):
#     return request.auth  # request.auth contains the authenticated user


from ninja import Router
from ninja.security import django_auth
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from apps.users.models import User
from apps.users.api.v1 import schemas

auth_router = Router()


@auth_router.get("/set-csrf-token")
def get_csrf_token(request):
    return {"csrftoken": get_token(request)}


@auth_router.post("/login")
def login_view(request, payload: schemas.UserIn):
    user = authenticate(request, username=payload.email, password=payload.password)
    if user is not None:
        login(request, user)
        return {"success": True}
    return {"success": False, "message": "Invalid credentials"}


@auth_router.post("/logout", auth=django_auth)
def logout_view(request):
    logout(request)
    return {"message": "Logged out"}


@auth_router.get("/user", auth=django_auth)
def user(request):
    secret_fact = (
        "The moment one gives close attention to any thing, even a blade of grass",
        "it becomes a mysterious, awesome, indescribably magnificent world in itself.",
    )
    return {
        "username": request.user.username,
        "email": request.user.email,
        "secret_fact": secret_fact,
    }


@auth_router.post("/register")
def register(request, payload: schemas.UserIn):
    try:
        User.objects.create_user(
            username=payload.email, email=payload.email, password=payload.password
        )
        return {"success": "User registered successfully"}
    except Exception as e:
        return {"error": str(e)}
