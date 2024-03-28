from apps.users.views import CenterView, EmailView, LogoutView, UserCountView, RegisterView, LoginView
from django.urls import path


urlpatterns = [
    path('usernames/<username:username>/count/', UserCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/', CenterView.as_view()),
    path('emails/', EmailView.as_view()),
    
]