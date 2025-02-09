from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "users"

    def __str__(self):
        return f"Username: {self.username} - Email: {self.email}"

    def __repr__(self):
        return f"{self.username} - {self.email}"
