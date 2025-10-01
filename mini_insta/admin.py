# File: mini_insta/admin.py
# Author: Louise Lee, llouise@bu.edu, 09/24/2025
# Description: What models we give admin access to

from django.contrib import admin

# Register your models here.

# give access to django admin to see profile model
from .models import Profile, Photo, Post

admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Post)
