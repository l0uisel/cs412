# File: restaurant/urls.py
# Author: Louise Lee, llouise@bu.edu, , 09/14/2025
# Description: Defines routing logic for quotes.
# Maps specific URL paths to view functions that handle specific requests

from django.urls import path  # from django urls library
from django.conf import settings  # include installed apps
from . import views  # from . = local directory

# URL patterns specific to the quotes app:
# Variable names django looks for
urlpatterns = [
    # path(r"", views.home, name="home"),  # connects empty string to views.home
    # when to use in front???
    path("", views.main_page, name="main_page"),
    path("main", views.main_page, name="main_page"),
    path("order", views.order, name="order_page"),
    path("confirmation", views.confirmation, name="confirmation_page"),
]
