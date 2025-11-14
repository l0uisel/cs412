# File: dadjokes/views.py
# Author: Louise Lee, llouise@bu.edu, 11/11/2025
# Description: Defines view function, handles rendering of the different pages by using
# context data
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Joke, Picture
import random
from rest_framework import generics
from .serializers import JokeSerializer, PictureSerializer


# Regular views for templates
class IndexView(DetailView):
    """Display one random Joke and one random Picture"""

    model = Joke
    template_name = "dadjokes/index.html"
    context_object_name = "joke"

    def get_object(self):
        """Return one Joke selected at random"""
        all_jokes = Joke.objects.all()
        return random.choice(all_jokes)

    def get_context_data(self, **kwargs):
        """Add a random Picture to the context"""
        context = super().get_context_data(**kwargs)
        all_pictures = Picture.objects.all()
        context["picture"] = random.choice(all_pictures)
        return context


class RandomView(DetailView):
    """Display one random Joke and one random Picture"""

    model = Joke
    template_name = "dadjokes/index.html"
    context_object_name = "joke"

    def get_object(self):
        """Return one Joke selected at random"""
        all_jokes = Joke.objects.all()
        return random.choice(all_jokes)

    def get_context_data(self, **kwargs):
        """Add a random Picture to the context"""
        context = super().get_context_data(**kwargs)
        all_pictures = Picture.objects.all()
        context["picture"] = random.choice(all_pictures)
        return context


class JokesView(ListView):
    """Display all Jokes"""

    model = Joke
    template_name = "dadjokes/jokes.html"
    context_object_name = "jokes"


class JokeView(DetailView):
    """Display a single Joke"""

    model = Joke
    template_name = "dadjokes/joke.html"
    context_object_name = "joke"


class PicturesView(ListView):
    """Display all Pictures"""

    model = Picture
    template_name = "dadjokes/pictures.html"
    context_object_name = "pictures"


class PictureView(DetailView):
    """Display a single Picture"""

    model = Picture
    template_name = "dadjokes/picture.html"
    context_object_name = "picture"


# REST API Views
class RandomJokeAPIView(generics.RetrieveAPIView):
    """API view to return one random Joke"""

    serializer_class = JokeSerializer

    def get_object(self):
        """Return one Joke selected at random"""
        all_jokes = Joke.objects.all()
        return random.choice(all_jokes)


class JokeListAPIView(generics.ListCreateAPIView):
    """API view to list all Jokes and create new Jokes"""

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveAPIView):
    """API view to return one Joke by primary key"""

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListAPIView):
    """API view to list all Pictures"""

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    """API view to return one Picture by primary key"""

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomPictureAPIView(generics.RetrieveAPIView):
    """API view to return one random Picture"""

    serializer_class = PictureSerializer

    def get_object(self):
        """Return one Picture selected at random"""
        all_pictures = Picture.objects.all()
        return random.choice(all_pictures)
