# serializers.py
from rest_framework import serializers
from authentication.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils import timezone


class LoginUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=60, write_only=True)
    email = serializers.EmailField(min_length=4, max_length=270)

    class Meta:
        model = User
        fields = ["email", "token", "user_type", "password"]
        read_only_fields = ["token", "user_type"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user: User = authenticate(email=email, password=password)

        if not user:
            raise exceptions.AuthenticationFailed("Invalid credentials")
        if not user.is_active:
            raise exceptions.AuthenticationFailed("Account disabled, contact admin")

        # Update last login time
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return {"email": user.email, "user_type": user.user_type, "token": user.token}


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    # TO DELETE ALL EXPIRED TOKENS STORED IN THE DB YOU CAN USE
    # python manage.py flushexpiredtokens
    default_error_messages = {"bad_token": ("Token is expired")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            self.fail("bad_token")


class CreationOfAccountsSerializer(serializers.Serializer):
    password = serializers.CharField(trim_whitespace=True, min_length=6)
    email = serializers.EmailField()

    def create(self, validated_data):
        user_type = self.context.get("user_type")

        if User.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError(detail={"message": "User already exists"})

        # Check if user_type is valid
        valid_user_types = dict(User.user_choices).keys()
        if user_type not in valid_user_types:
            raise serializers.ValidationError(
                f"Invalid user type. Choose from: {', '.join(valid_user_types)}"
            )

        # Use the generic create_admin method for all admin types
        return User.objects.create_admin(
            email=validated_data["email"],
            password=validated_data["password"],
            user_type=user_type,
        )


class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer for listing admin users"""

    class Meta:
        model = User
        fields = ["id", "email", "user_type", "created_at", "last_login", "is_active"]
        read_only_fields = ["id", "created_at", "last_login"]


# serializers.py - Add to your existing serializers.py file
from rest_framework import serializers
from authentication.models import User
from .models import PasswordResetToken
from django.utils import timezone
from django.urls import reverse


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Validate that the email exists in the system"""
        try:
            user = User.objects.get(email=value)
            # Check if the user is an admin (any type except regular users)
            if user.is_active:
                return value
            raise serializers.ValidationError("This account is inactive.")
        except User.DoesNotExist:
            # For security reasons, we don't reveal whether an email exists or not
            # We'll just proceed without an error, but won't send an email
            return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    password = serializers.CharField(min_length=6, write_only=True)
    confirm_password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        """Validate that the token exists and passwords match"""
        try:
            token_obj = PasswordResetToken.objects.get(token=attrs["token"])

            if not token_obj.is_valid:
                if token_obj.is_used:
                    raise serializers.ValidationError(
                        {"token": "This reset link has already been used."}
                    )
                else:
                    raise serializers.ValidationError(
                        {"token": "This reset link has expired."}
                    )

            if attrs["password"] != attrs["confirm_password"]:
                raise serializers.ValidationError(
                    {"password": "Passwords do not match."}
                )

            attrs["token_obj"] = token_obj
            return attrs

        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({"token": "Invalid reset token."})
