from ninja import Router
from ninja.security import django_auth
from apps.users.api.v1.schemas import UserOut, UserIn

router = Router()


@router.get("/users/me", response=UserOut, auth=django_auth)
def get_current_user(request):
    return request.auth


# Implement the login endpoint
@router.post("/login", response=UserOut)
def login(request, payload: UserIn):
    # Your login logic here
    pass


@router.post("/logout")
def logout(request):
    # Your logout logic here
    pass


@router.post("/register", response=UserOut)
def register(request, payload: UserIn):
    # Your registration logic here
    pass
