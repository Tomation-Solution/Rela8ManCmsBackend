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
        fields = ["email", "token", "user_type", "password"]
        read_only_fields = ["token", "user_type"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user: User = authenticate(email=email, password=password)
        # print({'user':user,"password":password,'email':email})
        if not user:
            raise exceptions.AuthenticationFailed("invalid Credentials")

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                "accout disabled, contact admin")

        return {
            "email": user.email,
            "user_type": user.user_type,
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


class CreationOfAccountsSerializer(serializers.Serializer):
    password = serializers.CharField(trim_whitespace=True)
    email = serializers.EmailField()

    def create(self, validated_data):
        user_type = self.context.get('user_type',)
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError(
                detail={'message': 'user exists'})
        if user_type == 'executive_secretary':
            return User.objects.create_executive_secretary(
                **validated_data,
            )
        else:
            raise ValueError("Please select right user type")
