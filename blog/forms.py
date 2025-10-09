# blog/forms.py
# define forms that we use for creation/update/delete operations

from django import forms

from .models import Article, Comment


class CreateArticleForm(forms.ModelForm):
    """A form to add Article to db"""

    class Meta:
        """Associate form w model from db"""

        model = Article
        # fields = ["author", "title", "text", "image_url"]
        fields = ["author", "title", "text", "image_file"]


class UpdateArticleForm(forms.ModelForm):
    """Handle update to article"""

    class Meta:
        """Associate with model" in db"""

        model = Article
        fields = ["title", "text"]  # fields allowing update


class CreateCommentForm(forms.ModelForm):
    """Associate this form with model from db"""

    class Meta:
        """Associate form w model from db"""

        model = Comment
        fields = ["author", "text"]
