# file explains how to convert Django data models for transmission as text over HTTP

from rest_framework import serializers
from .models import *


class ArticleSerializer(serializers.ModelSerializer):
    """A serializer class for the Article model.
    Specifies which fields are exposed in the API."""

    model = Article
    fields = ["id", "title", "text", "author", "published", "image_file"]

    # we can add extra code to execute
    # on CRUD operations

    def create(self, validated_data):
        """handle object creation"""
        print(f"ArticleSerializer.create(), validated_data={validated_data}.")

        # create Article object
        article = Article.objects.create(user=User.objects.first(), **validated_data)

        # attach FK of user
        # article.user = User.objects.first()

        # save to database
        article.save()

        # return article instance
        return article
