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
        logger.info("Start: %s", attrs)
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                email=username, password=password)

            serializer = UserSerializer(user)
            attrs['user'] = serializer.data
            logger.info(attrs)
            return attrs


class RefreshTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            token = Token.objects.get(key=attrs.get('token'))
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Token does not exist.')
        else:
            user = token.user
            token.delete()
            new_token = Token.objects.create(user=user)

        attrs['token'] = new_token
        attrs['user'] = UserSerializer(new_token.user).data
        return attrs
