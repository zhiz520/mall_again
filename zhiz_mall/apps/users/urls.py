from apps.users.views import AddressDeleteView, AddressUpdateView, EmailVerifyView,CenterView, EmailView, LogoutView, UserCountView, RegisterView, LoginView, AddressView, AddressDefaultView
from django.urls import path
from apps.users.views import AddressCreateView


urlpatterns = [
    path('usernames/<username:username>/count/', UserCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/', CenterView.as_view()),
    path('emails/', EmailView.as_view()),
    path('emails/verification/', EmailVerifyView.as_view()),
    path('addresses/create/', AddressCreateView.as_view()),
    path('addresses/', AddressView.as_view()),
    path('addresses/<address_id>/', AddressUpdateView.as_view()),
    path('addresses/<int:address_id>/', AddressDeleteView.as_view()),
    path('addresses/<address_id>/default/', AddressDefaultView.as_view()),
]