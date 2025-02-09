# from ninja import Router
# from apps.users.api.v1.schemas import UserIn, UserOut
# from django.shortcuts import get_object_or_404
# from .services import create_user
# from apps.users.models import User

# router = Router(tags=["Users"])


# @router.post("/register", response=UserOut)
# def register_user(request, data: UserIn):
#     return create_user(data)


# @router.get("/{user_id}", response=UserOut)
# def get_user_detail(request, user_id: int):
#     user = get_object_or_404(User, id=user_id)
#     return user


# apps/users/api/v1/endpoints.py
from ninja import Router
from .schemas import UserOut, UserIn  # Create these schema classes

router = Router()


@router.post("/", response={201: UserOut})
def create_user(request, payload: UserIn):
    # Your user creation logic here
    pass


@router.get("/{user_id}", response=UserOut)
def get_user(request, user_id: int):
    # Your user retrieval logic here
    pass
