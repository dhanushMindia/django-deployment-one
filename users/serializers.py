# users/serializers.py
from rest_framework import serializers
from .models import CustomUser, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('user', 'id')

class UserDetailSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'profile')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'date_of_birth')

    def create(self, validated_data):
        # Create user but set them as inactive until OTP verification
        user = CustomUser.objects.create_user(**validated_data, is_active=False)
        UserProfile.objects.create(user=user)
        return user