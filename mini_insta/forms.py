# File: mini_insta/forms.py
# Author: Louise Lee, llouise@bu.edu, 10/01/2025
# Description: Define forms that we use for creation/update/delete operations


# define forms that we use for creation/update/delete operations

from django import forms

from .models import *


class CreatePostForm(forms.ModelForm):
    """Form to add Post to database"""

    # Check do we require image url for every post
    image_url = forms.URLField(label="Image URL", required=False)

    class Meta:
        """Associate form with model from database"""

        model = Post
        # Image separate from Post model
        fields = ["caption"]
