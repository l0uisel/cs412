# blog/views.py
# views for blog application
from django.shortcuts import render
from django.views.generic import ListView  # look at all instances of model
from .models import Article


# Create your views here.
class ShowAllView(ListView):
    """Define a viw class to show all blog Articles."""

    # model name and template you want to use
    model = Article
    template_name = "blog/show_all.html"
    # variable within html page, contain many article instances
    context_object_name = "articles"
