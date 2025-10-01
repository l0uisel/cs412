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

    # Admin comment
    def __str__(self):
        """Return string rep of this model instance"""
        # Show username and display name
        return f"{self.username}, {self.display_name}"

    def get_all_posts(self):
        """Return Posts objects for profile"""
        posts = Post.objects.filter(profile=self)
        return posts


class Post(models.Model):
    """Encapsulate idea of posts on a user's profile"""

    # Data attributes for Post
    # If profile deleted, so will the posts
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    # Admin comment
    def __str__(self):
        """Return string rep of post"""
        return f"{self.profile.username}'s post"

    def get_all_photos(self):
        photos = Photo.objects.filter(post=self)
        return photos


class Photo(models.Model):
    """Encapsulated idea of photos with a user's post"""

    # Data attributes for Photo
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)  # can there be no image?
    timestamp = models.DateTimeField(auto_now_add=True)

    # Admin comment
    def __str__(self):
        return f"{self.post.profile.username} photo"
