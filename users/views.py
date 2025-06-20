# users/views.py
from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserDetailSerializer, UserProfileSerializer
# --- Add imports for sending email ---
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    # --- Add this method to send email on registration ---
    def perform_create(self, serializer):
        user = serializer.save()
        user.generate_otp() # Generate and save the OTP
        
        # --- Send OTP Email ---
        try:
            subject = 'Your OTP for Future Founders Co'
            html_message = render_to_string('users/welcome_email.html', {'user': user, 'otp': user.email_otp})
            plain_message = f'Your OTP is {user.email_otp}'
            
            send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)
        except Exception as e:
            print(f"Error sending OTP email to {user.email}: {e}")
class VerifyOTPView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({'error': 'Email and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active and user.is_email_verified:
             return Response({'message': 'User is already verified and active.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.email_otp != otp:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if timezone.now() > user.otp_expiry_time:
            return Response({'error': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        # OTP is correct, activate the user
        user.is_active = True
        user.is_email_verified = True
        user.email_otp = None  # Clear the OTP
        user.otp_expiry_time = None
        user.save()

        # You can optionally return JWT tokens here to log the user in immediately
        return Response({'message': 'Email verified successfully. You can now log in.'}, status=status.HTTP_200_OK)



class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile

class UserPublicProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class GoogleLoginView(SocialLoginView):
    """
    The view that handles the callback from Google. It takes the access token,
    verifies it with Google, and then logs in or creates a new user.
    """
    adapter_class = GoogleOAuth2Adapter
    # The callback URL you configured in your Google Cloud Console
    callback_url = "http://127.0.0.1:8000/accounts/google/login/callback/"
    # The client class handles the OAuth2 flow
    client_class = OAuth2Client