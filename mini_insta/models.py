# File: mini_insta/models.py
# Author: Louise Lee, llouise@bu.edu, 09/24/2025
# Description: Models define the fields (columns) of database, specifying data types, values, rules

from django.db import models
from django.urls import reverse


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

    def get_absolute_url(self):
        """Return URL to display one instance of object"""
        return reverse("show_profile", kwargs={"pk": self.pk})

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

    # def get_absolute_url(self):
    #     """Return URL to display one instance of object"""
    #     return reverse("post", kwargs={"pk": self.pk})

    def get_all_photos(self):
        photos = Photo.objects.filter(post=self)
        return photos


class Photo(models.Model):
    """Encapsulated idea of photos with a user's post"""

    # Data attributes for Photo
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)  # can there be no image?
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_image_url(self) -> str:
        """Prefer external URL; else use uploaded file URL; else a hard fallback."""
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return (
            "https://media.istockphoto.com/id/1472933890/vector/no-image-vector-symbol-"
            "missing-available-icon-no-gallery-for-this-moment-placeholder.jpg?s=612x612&w=0&k=20&"
            "c=Rdn-lecwAj8ciQEccm0Ep2RX50FCuUJOaEM8qQjiLL0="
        )

    # Admin comment
    def __str__(self):
        return f"{self.post.profile.username} photo"
