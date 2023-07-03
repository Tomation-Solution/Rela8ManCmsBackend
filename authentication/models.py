from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, user_type, password=None):
        if email is None:
            raise ValueError("User should have an email")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.user_type = user_type
        user.save()

        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise ValueError("Super User must have a password")

        user = self.create_user(email, password)
        user.user_type = "super_user"
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(PermissionsMixin, AbstractBaseUser):
    user_choices = [
        ("publication_news", "publication_news"),
        ("event_training", "event_training"),
        ("public_view", "public_view"),
        ("registrations_payments", "registrations_payments"),
        ("prospective_certificates", "prospective_certificates"),
        ("super_user", "super_user"),
        ("executive_secretary", "executive_secretary"),
    ]

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_type = models.CharField(choices=user_choices, max_length=200)
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
