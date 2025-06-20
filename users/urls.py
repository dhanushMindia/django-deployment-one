# users/urls.py
from django.urls import path
from .views import UserRegistrationView, UserProfileDetailView, UserPublicProfileView, VerifyOTPView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'), # New URL
    path('profile/', UserProfileDetailView.as_view(), name='user-profile'),
    path('<int:pk>/profile/', UserPublicProfileView.as_view(), name='user-public-profile'),
]