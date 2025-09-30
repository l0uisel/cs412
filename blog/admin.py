from django.contrib import admin

# Register your models here.

# give access to django admin to see article model
from .models import Article, Comment

admin.site.register(Article)
admin.site.register(Comment)
