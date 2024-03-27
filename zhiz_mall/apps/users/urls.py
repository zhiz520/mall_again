from apps.users.views import ImageCodeView, UserCountView, RegisterView
from django.urls import path


urlpatterns = [
    path('usernames/<username:username>/count/', UserCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('image_codes/<uuid>/', ImageCodeView.as_view()),
    
]