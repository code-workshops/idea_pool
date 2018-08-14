from django.urls import path

from .views import UserListCreateAPIView, UserRetrieveEditAPIView

urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='users'),
    path('<uid>/', UserRetrieveEditAPIView.as_view(), name='user-detail'),
]
