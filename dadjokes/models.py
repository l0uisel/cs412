# File: dadjokes/models.py
# Author: Louise Lee, llouise@bu.edu, 11/11/2025
# Description: Models define the fields (columns) of database, specifying data types, values, rules

from django.db import models
from django.urls import reverse


class Joke(models.Model):
    """Encapsulate data of a dad joke"""

    text = models.TextField(blank=False)
    contributor = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string rep of this model instance"""
        return f"{self.text[:50]}... by {self.contributor}"

    def get_absolute_url(self):
        """Return URL to display one instance of object"""
        return reverse("joke", kwargs={"pk": self.pk})


class Picture(models.Model):
    """Encapsulate data of a silly picture or GIF"""

    image_url = models.URLField(blank=False)
    contributor = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string rep of this model instance"""
        return f"Picture by {self.contributor}"

    def get_absolute_url(self):
        """Return URL to display one instance of object"""
        return reverse("picture", kwargs={"pk": self.pk})
