# File: mini_insta/models.py
# Author: Louise Lee, llouise@bu.edu, 09/24/2025
# Description: Models define the fields (columns) of database, specifying data types, values, rules

from django.db import models


# Create your models here.
class Profile(models.Model):
    """Encapsulate data of individual profile"""

    # Define data attributes of the Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now_add=True)

    # Comment
    def __str__(self):
        """Return string rep of this model instance"""
        # Show username and display name
        return f"{self.username}, {self.display_name}"
