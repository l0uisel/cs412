from django.db import models


# Create your models here.
class Article(models.Model):
    """Encapsulate data of blog Article by an author"""

    # define data attributes of the Article object
    title = models.TextField(blank=True)  # can create title even if empty
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)  # set time to now
