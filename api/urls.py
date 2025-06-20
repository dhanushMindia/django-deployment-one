# api/urls.py
from django.urls import path
from .views import CompetitionListView, CompetitionDetailView

urlpatterns = [
    # URL for the list view, e.g., /api/competitions/
    path('competitions/', CompetitionListView.as_view(), name='competition-list'),
    
    # URL for the detail view, e.g., /api/competitions/1/
    # The <int:pk> part captures the ID from the URL.
    path('competitions/<int:pk>/', CompetitionDetailView.as_view(), name='competition-detail'),
]
