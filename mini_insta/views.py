# File: quotes/views.py
# Author: Louise Lee, llouise@bu.edu, 09/25/2025
# Description: Defines view function, handles rendering of the different pages by using
# context data

from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)  # look at all instances of model (detail = single instance)
from .models import Profile
import random


# Create your views here.
class ProfileListView(ListView):
    """Define a viw class to show all profiles."""

    # model name and template you want to use
    model = Profile
    template_name = "profile/show_all_profiles.html"
    # variable within html page, contain many profile instances
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """Display a single profile"""

    model = Profile
    template_name = "profile/show_profile.html"
    context_object_name = "profile"


# class RandomArticleView(DetailView):
#     """Display single article selected at random"""

#     model = Article
#     template_name = "blog/article.html"
#     context_object_name = "article"

#     # methods
#     def get_object(self):
#         """Return one instance of the Article object selected at random"""
#         all_articles = Article.objects.all()
#         article = random.choice(all_articles)
#         return article
