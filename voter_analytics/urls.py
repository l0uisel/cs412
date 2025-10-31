# File: voter_analytics/urls.py
# Author: Louise Lee, llouise@bu.edu, 10/28/2025
# Description: Defines routing logic for quotes.
# Maps specific URL paths to view functions that handle specific requests

from django.urls import path
from . import views

urlpatterns = [
    path(r"", views.VoterListView.as_view(), name="voters"),
    path(r"voter/<int:pk>", views.VoterDetailView.as_view(), name="voter"),
    path(r"graphs", views.GraphsView.as_view(), name="graphs"),
]
