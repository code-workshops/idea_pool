from django.urls import include, path

app_name = 'idea_pool'

urlpatterns = [
    path('ideas/', include('ideas.urls'), name='ideas'),
    path('users/', include('accounts.urls'), name='users'),
]
