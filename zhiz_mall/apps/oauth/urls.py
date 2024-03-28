from django.urls import path
from oauth.views import OauthQQView, QQLoginUrlView


urlpatterns = [
    path('qq/authorization/', QQLoginUrlView.as_view()),
    path('oauth_callback/', OauthQQView.as_view()),
]