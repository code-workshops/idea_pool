from django.urls import path

from .views import IdeaListCreateAPIView, IdeaRetrieveEditAPIView

urlpatterns = [
    path('', IdeaListCreateAPIView.as_view(), name='ideas'),
    path('<uid>/', IdeaRetrieveEditAPIView.as_view(), name='idea-detail'),
]
