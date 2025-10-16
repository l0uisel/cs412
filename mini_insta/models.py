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

    # Following accessor methods
    def get_followers(self):
        """Return Follower objects for profile"""
        followers = Follow.objects.select_related("follower_profile").filter(
            profile=self
        )
        return [p.follower_profile for p in followers]

    def get_num_followers(self):
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        followers = Follow.objects.select_related("profile").filter(
            follower_profile=self
        )
        return [p.profile for p in followers]  # list[Profile]

    def get_num_following(self):
        return Follow.objects.filter(follower_profile=self).count()

    def get_num_posts(self):
        return Post.objects.filter(profile=self).count()

    def __str__(self):
        return self.username


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
        return f"{self.profile.username}'s post {self.pk}"

    # def get_absolute_url(self):
    #     """Return URL to display one instance of object"""
    #     return reverse("post", kwargs={"pk": self.pk})

    # Comments accessor methods
    def get_all_photos(self):
        photos = Photo.objects.filter(post=self)
        return photos

    def get_all_comments(self):
        return list(
            Comment.objects.select_related("profile")
            .filter(post=self)
            .order_by("timestamp")
        )

    # Likes accessor methods
    def get_likes(self):
        return list(Like.objects.select_related("profile").filter(post=self))

    def get_num_likes(self):
        return Like.objects.filter(post=self).count()


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


class Follow(models.Model):
    """Encapsulated idea of an edge connecting two nodes on mini_insta(profile follow another)"""

    # Data attributes for Follow
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile"
    )
    follower_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="follower_profile"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("profile", "follower_profile")  # no dupes
        ordering = ["-timestamp"]

    # Admin comment
    def __str__(self):
        publisher = self.profile.username
        subcriber = self.follower_profile.username
        return f"{subcriber} followed {publisher}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ["timestamp"]  # oldest to newest

    def __str__(self):
        return f"Comment by {self.profile.username} on Post {self.post.pk}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "profile")  # one like per user per post
        ordering = ["-timestamp"]  # newest to oldest

    def __str__(self):
        who = getattr(self.profile, "display_name", None) or self.profile.username
        return f"{self.profile.username} liked Post {self.post.pk}"
