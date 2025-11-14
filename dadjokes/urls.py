# File: dadjokes/urls.py
# Author: Louise Lee, llouise@bu.edu, 11/11/2025
# Description: Defines routing logic for quotes.
# Maps specific URL paths to view functions that handle specific requests

from django.urls import path
from .views import *

urlpatterns = [
    # Regular views
    path("", IndexView.as_view(), name="index"),
    path("random", RandomView.as_view(), name="random"),
    path("jokes", JokesView.as_view(), name="jokes"),
    path("joke/<int:pk>", JokeView.as_view(), name="joke"),
    path("pictures", PicturesView.as_view(), name="pictures"),
    path("picture/<int:pk>", PictureView.as_view(), name="picture"),
    # API endpoints
    path("api/", RandomJokeAPIView.as_view(), name="api_random_joke"),
    path("api/random", RandomJokeAPIView.as_view(), name="api_random_joke_alt"),
    path("api/jokes", JokeListAPIView.as_view(), name="api_jokes"),
    path("api/joke/<int:pk>", JokeDetailAPIView.as_view(), name="api_joke"),
    path("api/pictures", PictureListAPIView.as_view(), name="api_pictures"),
    path("api/picture/<int:pk>", PictureDetailAPIView.as_view(), name="api_picture"),
    path(
        "api/random_picture", RandomPictureAPIView.as_view(), name="api_random_picture"
    ),
]
