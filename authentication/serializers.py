from rest_framework import serializers
from authentication.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class LoginUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6, max_length=60, write_only=True)
    email = serializers.EmailField(min_length=4, max_length=270)

    class Meta:
        model = User
        fields = ["email", "token", "password"]
        read_only_fields = ["token"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user: User = authenticate(email=email, password=password)

        if not user:
            raise exceptions.AuthenticationFailed("invalid Credentials")

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                "accout disabled, contact admin")

        return {
            "email": user.email,
            "token": user.token
        }


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
        except TokenError as exc:
            self.fail("bad_token")
