# File: mini_insta/views.py
# Author: Louise Lee, llouise@bu.edu, 09/25/2025
# Description: Defines view function, handles rendering of the different pages by using
# context data

from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)  # look at all instances of model (detail = single instance)
from .models import Profile, Post


# Create your views here.
class ProfileListView(ListView):
    """Define a view class to show all profiles."""

    # model name and template you want to use
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    # variable within html page, contain many profile instances
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """Display a single profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"


class PostDetailView(DetailView):
    """Display a single post"""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"
