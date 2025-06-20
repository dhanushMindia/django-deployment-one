# api/views.py
from rest_framework import generics
from .models import Competition
from .serializers import CompetitionListSerializer, CompetitionDetailSerializer

class CompetitionListView(generics.ListAPIView):
    """
    An API endpoint that provides a list of all competitions.
    Uses the lightweight serializer for performance.
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionListSerializer

class CompetitionDetailView(generics.RetrieveAPIView):
    """
    An API endpoint that provides the full details for a single competition,
    retrieved by its primary key (ID).
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionDetailSerializer
