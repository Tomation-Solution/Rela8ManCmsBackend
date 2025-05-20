# models.py
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, email, user_type, password=None):
        if email is None:
            raise ValueError("User should have an email")
        if password is None:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.user_type = user_type
        user.save()

        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise ValueError("Super User must have a password")

        user = self.create_user(email, user_type="super_user", password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True  # the superuser has to be active when created
        user.save()

        return user

    def create_executive_secretary(self, email, password):
        if password is None:
            raise ValueError("Executive Secretary User Must have A Password")

        user = self.create_user(email, "executive_secretary", password)
        user.is_active = True
        user.save()

        return user

    # Added method to create admin user of any type
    def create_admin(self, email, user_type, password):
        if password is None:
            raise ValueError("Admin User Must have A Password")

        if user_type not in dict(User.user_choices).keys():
            raise ValueError(f"Invalid user type: {user_type}")

        user = self.create_user(email, user_type, password)
        user.is_active = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
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
    last_login = models.DateTimeField(
        null=True, blank=True
    )  # Added to track last login

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email}"

    @property
    def token(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            "access": str(refresh_token.access_token),
            "refresh": str(refresh_token),
        }


# models.py - Add to your existing models.py file
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta
from authentication.models import User


class PasswordResetToken(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="password_reset_tokens"
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.token}"

    def save(self, *args, **kwargs):
        # Set expiration time if not already set
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        """Check if token is valid (not expired and not used)"""
        return not self.is_used and timezone.now() < self.expires_at
