# blog/views.py
# views for blog application
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
)  # look at all instances of model (detail = single instance)
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse
import random


# Create your views here.
class ShowAllView(ListView):
    """Define a viw class to show all blog Articles."""

    # model name and template you want to use
    model = Article
    template_name = "blog/show_all.html"
    # variable within html page, contain many article instances
    context_object_name = "articles"


class ArticleView(DetailView):
    """Display a single article"""

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"


class RandomArticleView(DetailView):
    """Display single article selected at random"""

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    # methods
    def get_object(self):
        """Return one instance of the Article object selected at random"""
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article


# subclass of CreateView to handle cretion of Article objects
class CreateArticleView(CreateView):
    """view to handle creation of new Atticle
    1) diplay HTML form to user nd 2) pocess form submission and store new Article (POST)
    """

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"


class CreateCommentView(CreateView):
    """View to handle creation of a new comment on an article"""

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        """Provide URL to redirect to after create new comment"""
        # create and return URL
        # return reverse("show_all")
        pk = self.kwargs["pk"]
        return reverse("article", kwargs={"pk": pk})

    def form_valid(self, form):
        """Method handles form submissino, save new object to Django db.
        We need to add the foreign key (of article) to Comment
        object before saving to db"""

        print(form.cleaned_data)
        # retrieve PK from URL pattern
        pk = self.kwargs["pk"]
        article = Article.objects.get(pk=pk)
        form.instance.article = article  # set the FK

        # delefate work to superclass form_valid method
        return super().form_valid(form)
