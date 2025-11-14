# File: dadjokes/serializers.py
# Author: Louise Lee, llouise@bu.edu, 11/12/2025
# Description: Explains how to convert Django data models for transmission as text over HTTP

from rest_framework import serializers
from .models import Joke, Picture


class JokeSerializer(serializers.ModelSerializer):
    """A serializer class for the Joke model."""

    class Meta:
        model = Joke
        fields = ["id", "text", "contributor", "created"]

    def create(self, validated_data):
        """Handle object creation"""
        print(f"JokeSerializer.create(), validated_data={validated_data}.")

        joke = Joke.objects.create(**validated_data)
        joke.save()

        return joke


class PictureSerializer(serializers.ModelSerializer):
    """A serializer class for the Picture model."""

    class Meta:
        model = Picture
        fields = ["id", "image_url", "contributor", "created"]
