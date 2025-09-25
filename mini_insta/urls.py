# File: mini_insta/urls.py
# Author: Louise Lee, llouise@bu.edu, 09/24/2025
# Description: Defines routing logic for quotes.
# Maps specific URL paths to view functions that handle specific requests

from django.urls import path  # from django urls library
from django.conf import settings  # include installed apps
from .views import (
    ShowAllView,
    ArticleView,
    RandomArticleView,
)  # from . = local directory

# URL patterns specific to the restaurant app:
# Variable names django looks for
urlpatterns = [
    path("", ShowAllView.as_view(), name="show_all_profiles"),
    # display signle article by primary key
    path("profile/<int:pk>", ProfileView.as_view(), name="profile"),
]
