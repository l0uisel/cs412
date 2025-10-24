# File: mini_insta/models.py
# Author: Louise Lee, llouise@bu.edu, 09/24/2025
# Description: Models define the fields (columns) of database, specifying data types, values, rules

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    """Encapsulate data of individual profile"""

    # Define data attributes of the Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="profiles",
        default=1,  # temporary default to handle existing rows (e.g., admin id=1)
    )

    # Admin comment
    def __str__(self):
        """Return string rep of this model instance"""
        # Show username and display name
        return f"{self.username}, {self.display_name}"

    def get_absolute_url(self):
        return reverse("show_profile", kwargs={"pk": self.pk})

    def get_all_posts(self):
        return Post.objects.filter(profile=self).order_by("-timestamp")

    # Following accessor methods
    def get_followers(self):
        """Return list of Profile objects that follow this profile"""
        follow_objs = Follow.objects.select_related("follower").filter(followed=self)
        return [f.follower for f in follow_objs]

    def get_num_followers(self):
        return Follow.objects.filter(followed=self).count()

    def get_following(self):
        """Return list of Profile objects that this profile follows"""
        follow_objs = Follow.objects.select_related("followed").filter(follower=self)
        return [f.followed for f in follow_objs]

    def get_num_following(self):
        return Follow.objects.filter(follower=self).count()

    def get_num_posts(self):
        return Post.objects.filter(profile=self).count()

    def get_post_feed(self):
        """Return posts from profiles that this profile follows"""
        followed_ids = Follow.objects.filter(follower=self).values_list(
            "followed_id", flat=True
        )
        return Post.objects.filter(profile_id__in=followed_ids).order_by("-timestamp")


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
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(upload_to="photos/", blank=True, null=True)
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


class Comment(models.Model):
    """Comment on a post"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ["timestamp"]  # oldest to newest

    def __str__(self):
        return f"Comment by {self.profile.username} on Post {self.post.pk}"


class Follow(models.Model):
    """A follows B"""

    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="following"
    )
    followed = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="followers"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "followed"], name="unique_follow"
            ),
            models.CheckConstraint(
                check=~models.Q(follower=models.F("followed")), name="no_self_follow"
            ),
        ]

    def __str__(self):
        return f"{self.follower.username} -> {self.followed.username}"


class Like(models.Model):
    """Profile likes a post"""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["profile", "post"], name="unique_like"),
        ]

    def __str__(self):
        return f"{self.profile.username} ♥ {self.post.id}"
