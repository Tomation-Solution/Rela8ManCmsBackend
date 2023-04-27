from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise ValueError("User should have an email")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise ValueError("Super User must have a password")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email}"

    @property
    def token(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            "access": str(refresh_token.access_token),
            "refresh": str(refresh_token)
        }
