# api/serializers.py
from rest_framework import serializers
from .models import Competition

class CompetitionListSerializer(serializers.ModelSerializer):
    """
    A lightweight serializer that only includes the competition's ID and title.
    """
    class Meta:
        model = Competition
        fields = ['id', 'title']

class CompetitionDetailSerializer(serializers.ModelSerializer):
    """
    A complete serializer that includes all fields for a single competition.
    """
    class Meta:
        model = Competition
        fields = '__all__'
