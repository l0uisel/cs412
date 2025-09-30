from django.db import models
from django.urls import reverse


# Create your models here.
class Article(models.Model):
    """Encapsulate data of blog Article by an author"""

    # define data attributes of the Article object
    title = models.TextField(blank=True)  # can create title even if empty
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)  # set time to now
    image_url = models.URLField(
        blank=True
    )  # makemigrations and migrate when change attributions

    # Indent into Article class
    def __str__(self):
        """Return string rep of this model instance"""
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        """Return URL to display one instance of object"""
        return reverse("article", kwargs={"pk": self.pk})

    def get_all_comments(self):
        """Return queryset of comments about article"""
        comments = Comment.objects.filter(article=self)
        return comments


class Comment(models.Model):
    """Encapsulate idea of a comment about article"""

    # data attribute fo comments
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string rep of comment"""
        return f"{self.text}"
