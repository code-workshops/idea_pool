from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.decorators import permission_classes as permissions
from rest_framework.permissions import AllowAny, IsAdminUser

from .serializers import User, UserSerializer


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    # @permissions(IsAdminUser)
    # def get(self, request, *args, **kwargs):
    #     pass


class UserRetrieveEditAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uid'
