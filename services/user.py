from django.contrib.auth import get_user_model
from django.db import models


def create_user(username: str, password: str, **kwargs) -> models.Model:
    return get_user_model().objects.create_user(
        username=username, password=password, **kwargs
    )


def get_user(user_id: int = None, username: str = None) -> models.Model:
    if user_id is None and username is None:
        raise ValueError("Either user_id or username must be provided")
    user_model = get_user_model()
    if user_id is not None:
        return user_model.objects.get(id=user_id)
    return user_model.objects.get(username=username)


def update_user(
    user_id: int = None,
    username: str = None,
    password: str = None,
    **kwargs,
) -> models.Model:
    user = get_user(user_id=user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    if username:
        user.username = username
    if password:
        user.set_password(password)
    user.save()
    return user
