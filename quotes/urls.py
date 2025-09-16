# File: quotes/urls.py
# Author: Louise Lee, llouise@bu.edu, 09/07/2025
# Description: Defines routing logic for quotes.
# Maps specific URL paths to view functions that handle specific requests

from django.urls import path  # from django urls library
from django.conf import settings  # include installed apps
from . import views  # from . = local directory

# URL patterns specific to the quotes app:
# Variable names django looks for
urlpatterns = [
    # Self-note: path(r"", views.home, name="home"),  # connects empty string to views.home
    # when to use in front??? - ANS: both fine
    path(r"", views.home_page, name="home_page"),
    path(r"quote", views.home_page, name="home_page"),
    path(r"show_all", views.show_all, name="show_all_page"),
    path(r"about", views.about, name="about_page"),
]
