from apps.users.views import UserCountView, RegisterView, LoginView
from django.urls import path


urlpatterns = [
    path('usernames/<username:username>/count/', UserCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    
    
]