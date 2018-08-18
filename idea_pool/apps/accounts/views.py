import copy
import logging
import jwt

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import JWTAuthentication, prepare_jwt
from .serializers import User, UserSerializer, AuthTokenSerializer

logger = logging.getLogger('idea_pool.accounts.views')


class AuthTokenView(APIView, DestroyModelMixin):
    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        """Authenticate user and return JWT, refresh."""
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        logger.info("user data: %s ", payload)
        user = User.objects.get(email=serializer.validated_data['email'])
        jwt_token = prepare_jwt(payload)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'jwt': jwt_token, 'refresh_token': token.key},
                        status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        data = request.data.get('refresh_token')
        try:
            token = Token.objects.get(key=data)
        except ObjectDoesNotExist:
            logger.info("Token not found.")
            raise
        else:
            token.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)


class RefreshTokenView(APIView):
    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        """Validate refresh token and return JWT, new refresh."""
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = serializer.validated_data['token'].key
        jwt_token = jwt.encode(user, settings.JWT_SECRET, algorithm='HS256')
        return Response({'jwt': jwt_token, 'refresh_token': token})


class UserDashboardView(RetrieveUpdateDestroyAPIView):
    """For me/ API requests."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        return self.request.user


class UserListCreateAPIView(ListCreateAPIView):
    """For users/ API requests."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        logger.info("Creating with: %s", request.data)
        payload = copy.copy(request.data)
        response = super(UserListCreateAPIView, self).post(request)
        if response.status_code == status.HTTP_201_CREATED:
            logger.info("Data: %s", response.data)
            jwt_token = prepare_jwt(payload)
            user = User.objects.get(email=payload['email'])
            token = Token.objects.create(user=user)
            tokens = {
                'jwt': jwt_token,
                'refresh_token': token.key}
            return Response(tokens, status=status.HTTP_201_CREATED)
        else:
            logger.debug("Request data: %s | User: %s", (request.data, request.user))
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveEditAPIView(RetrieveUpdateDestroyAPIView):
    """For api/v1/ requests."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uid'
