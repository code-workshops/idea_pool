import logging

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User

logger = logging.getLogger('idea_pool.accounts.serializers')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'email', 'avatar_url',)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        logger.info(attrs)
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                email=username, password=password)
        else:
            serializers.ValidationError('User authentication failed.')
        serializer = UserSerializer(user)
        attrs['user'] = serializer.data
        attrs['refresh_token'], created = Token.objects.get_or_create(user=user)
        logger.info(attrs['user'])
        return attrs


class RefreshTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            token = Token.objects.get(key=attrs.get('token'))
        except Exception as exc:
            raise serializers.ValidationError('Token does not exist.')
        else:
            user = token.user
            token.delete()
            new_token = Token.objects.create(user=user)


        attrs['token'] = new_token
        attrs['user'] = UserSerializer(new_token.user).data
        return attrs
