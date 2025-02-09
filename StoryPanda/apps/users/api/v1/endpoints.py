from ninja import Router
from .schemas import UserOut, UserIn

router = Router()


@router.post("/", response={201: UserOut})
def create_user(request, payload: UserIn):
    # Your user creation logic here
    pass


@router.get("/{user_id}", response=UserOut)
def get_user(request, user_id: int):
    # Your user retrieval logic here
    pass
