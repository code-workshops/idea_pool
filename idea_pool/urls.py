"""idea_pool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from accounts.views import (AuthTokenView, RefreshTokenView, UserDashboardView,
                            UserListCreateAPIView)
from ideas.views import IdeaDashboardView, IdeaListView

urlpatterns = [
    path('admin', admin.site.urls),
    path('docs', include_docs_urls(title="Idea Pool API")),
    path('api-auth', include('rest_framework.urls')),
    path('api/v1', include('api_urls', namespace='api')),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),

    path('access-tokens', AuthTokenView.as_view()),
    path('access-tokens/refresh', RefreshTokenView.as_view()),

    path('me', UserDashboardView.as_view(), name='dashboard'),
    path('users', UserListCreateAPIView.as_view(), name='users-create'),
    path('ideas/<uid>', IdeaDashboardView.as_view(), name='ideas-detail'),
    path('ideas', IdeaListView.as_view(), name='ideas-dash'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
