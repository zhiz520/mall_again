from apps.users.views import UserCountView, RegisterView
from django.urls import path


urlpatterns = [
    path('usernames/<username:username>/count/', UserCountView.as_view()),
    path('register/', RegisterView.as_view()),

]