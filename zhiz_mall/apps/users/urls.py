from apps.users.views import UserCountView
from django.urls import path


urlpatterns = [
    path('usernames/<username:username>/count/', UserCountView.as_view()),
    
]