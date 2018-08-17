import logging

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from accounts.auth import JWTAuthentication
from .serializers import Idea, IdeaSerializer

logger = logging.getLogger('idea_pool.ideas.views')


class IdeaListView(ListCreateAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    lookup_field = 'uid'

    def get(self, request, *args, **kwargs):
        ideas = self.get_queryset().order_by('-average_score')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(ideas, request)
        serializer = self.get_serializer(result_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug("Request data: %s | User: %s", (request.data, request.user))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IdeaDashboardView(RetrieveUpdateDestroyAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    lookup_field = 'uid'


class IdeaListCreateAPIView(ListCreateAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        # TODO: order_by("-average_score") is not reversing order.
        ideas = self.get_queryset().order_by("-average_score")
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(ideas, request)
        serializer = self.get_serializer(result_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IdeaRetrieveEditAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'uid'
