import logging

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User

logger = logging.getLogger('idea_pool.accounts.serializers')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False, write_only=True
    )
    name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    avatar_url = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('name', 'email', 'avatar_url', 'password',)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], **validated_data)
        logger.debug("UserSerializer created: %s", user)
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        logger.debug("Start: %s", attrs)
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                email=username, password=password)
            if user:
                serializer = UserSerializer(user)
                attrs['user'] = serializer.data
                return attrs
            else:
                raise serializers.ValidationError('Invalid login credentials.')


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        try:
            token = Token.objects.get(key=attrs.get('refresh_token'))
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Token does not exist.')
        else:
            user = token.user

        attrs['user'] = UserSerializer(user).data
        return attrs
