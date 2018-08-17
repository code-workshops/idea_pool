import jwt, logging

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

logger = logging.getLogger('idea_pool.accounts.auth')


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        # returns 'Token XXXXXXXXXXX'
        jwt_value = request.META.get('HTTP_AUTHORIZATION', b'').split()

        if jwt_value is None or len(jwt_value) == 0:
            return None

        try:
            payload = jwt.decode(jwt_value[0], settings.JWT_SECRET,
                                 algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed('Signature expired.')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Error decoding.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return (user, jwt_value)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        username = payload.get('email')

        if not username:
            raise exceptions.AuthenticationFailed('Invalid payload.')

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid signature.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('Account disabled.')

        return user
