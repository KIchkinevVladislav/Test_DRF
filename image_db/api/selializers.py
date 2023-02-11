import random

from rest_framework import serializers
from rest_framework.exceptions import (
    ValidationError,)
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from .models import User, Image

def get_tokens_for_user(user):
    """
    Creating a token for the user manually.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def generate_code():
    """
    Code generation for confirmation_code.
    """
    random.seed()
    return str(random.randint(10000000, 99999999))


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serialization of data during user registration.
    Create confirmation_code.
    """
    class Meta:
        model = User
        fields = ('email',)

    def validate(self, data):
        confirmation_code = generate_code()
        data['confirmation_code'] = confirmation_code
        return data


class TokenSerializer(serializers.ModelSerializer):
    """
    Serialization at user login.
    Checking the confirmation_code.
    """
    email = serializers.EmailField()

    
    class Meta:
        model = User
        fields = (
            'email',
            'confirmation_code',
        )

    def validate(self, data):
        email = data['email']
        confirmation_code = data['confirmation_code']
        profile = get_object_or_404(User, email=email)
        if profile.confirmation_code != confirmation_code:
            raise ValidationError('ошибка')
        else:
            token = get_tokens_for_user(profile)
            data['token'] = token
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        fields = ('email', 'username', 'role', 'first_name', 'last_name',)
        model = User


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        field = '__all__'
