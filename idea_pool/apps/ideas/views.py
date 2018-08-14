from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status

from .serializers import Idea, IdeaSerializer


class IdeaListCreateAPIView(ListCreateAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        ideas = self.get_queryset().order_by('score__average')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(ideas, request)
        serializer = self.get_serializer(result_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IdeaRetrieveEditAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissions,)
    lookup_field = 'uid'
