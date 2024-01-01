from attr import fields
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    default_error_messages = {
        'no_active_account': 'No active account found with the given credentials.'
    }

    def validate(self, attr):
        email = attr.get('email', None)
        password = attr.get('password', None)

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(self.default_error_messages)

        refresh_token = RefreshToken.for_user(user)
        user.last_login = timezone.now()
        user.save()
        return {
            'token': str(refresh_token.access_token),
            'refresh': str(refresh_token),
        }


class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    default_error_messages = {'refresh': 'Invalid parameter is sent.'}

    def validate(self, attr):
        self.refresh = attr.get('refresh', None)
        if self.refresh is None:
            raise serializers.ValidationError(self.default_error_messages)
        return attr

    def save(self, **kwargs):
        RefreshToken(self.refresh).blacklist()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User(email=email, **validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
