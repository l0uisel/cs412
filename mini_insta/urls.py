# File: mini_insta/urls.py
# Author: Louise Lee, llouise@bu.edu, 09/24/2025
# Description: Defines routing logic for quotes.
# Maps specific URL paths to view functions that handle specific requests

from django.urls import path  # from django urls library
from django.conf import settings  # include installed apps
from .views import (
    ProfileListView,
    ProfileDetailView,
    PostDetailView,
    CreatePostView,
    UpdateProfileView,
    DeletePostView,
    UpdatePostView,
    ShowFollowersDetailView,
    ShowFollowingDetailView,
)  # from . = local directory

# URL patterns specific to the restaurant app:
# Variable names django looks for
urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    # display signle article by primary key
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>", PostDetailView.as_view(), name="show_post"),
    path("profile/<int:pk>/create_post", CreatePostView.as_view(), name="create_post"),
    path("profile/<int:pk>/update", UpdateProfileView.as_view(), name="update_profile"),
    path("post/<int:pk>/delete/", DeletePostView.as_view(), name="delete_post"),
    path("post/<int:pk>/update/", UpdatePostView.as_view(), name="update_post"),
    path(
        "profile/<int:pk>/followers",
        ShowFollowersDetailView.as_view(),
        name="show_followers",
    ),
    path(
        "profile/<int:pk>/following",
        ShowFollowingDetailView.as_view(),
        name="show_following",
    ),
]
