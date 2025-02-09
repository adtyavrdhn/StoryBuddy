from apps.users.models import User


def create_user(data):
    return User.objects.create(**data.dict())


def get_user(user_id):
    return User.objects.get(id=user_id)
