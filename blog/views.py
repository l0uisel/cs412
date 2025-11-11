# blog/views.py
# views for blog application
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)  # look at all instances of model (detail = single instance)
from .models import Article, Comment
from .forms import (
    CreateArticleForm,
    CreateCommentForm,
    UpdateArticleForm,
)
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin  # for authentication
from django.contrib.auth.forms import UserCreationForm  # for new User
from django.contrib.auth.models import User  # Django user model
import random


# Create your views here.
class ShowAllView(ListView):
    """Define a viw class to show all blog Articles."""

    # model name and template you want to use
    model = Article
    template_name = "blog/show_all.html"
    # variable within html page, contain many article instances
    context_object_name = "articles"

    def dispatch(self, request, *args, **kwargs):
        """Override the dispatch method to add debugging information."""

        if request.user.is_authenticated:
            print(f"ShowAllView.dispatch(): request.user={request.user}")
        else:
            print(f"ShowAllView.dispatch(): not logged in.")

        return super().dispatch(request, *args, **kwargs)


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

    def form_valid(self, form):
        """Override the default method to add some debug info"""
        # print out form data
        print(f"CreateArticleView.form_valid(): {form.clenaed_data}")
        # delegate work to superclass
        return super().form_valid(form)


class CreateCommentView(LoginRequiredMixin, CreateView):
    """View to handle creation of a new comment on an article"""

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_login_url(self):
        """Return the URL for this app's login page"""
        return reverse("login")

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

        print(f"CreateArticleView: form.cleaned_data={form.cleaned_data}")

        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")

        # attach user to form instance (Article object):
        form.instance.user = user

        return super().form_valid(form)


class UpdateArticleView(UpdateView):
    """View class to handle update of article based on PK"""

    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"


class DeleteCommentView(DeleteView):
    """View class to handle comment deletion for Article"""

    model = Comment
    template_name = "blog/delete_comment_form.html"

    def get_success_url(self):
        """Return URL ot redirect after successful delete"""
        # find PK for Comment
        pk = self.kwargs["pk"]
        comment = Comment.objects.get(pk=pk)

        article = comment.article
        return reverse("article", kwargs={"pk": article.pk})


class UserRegistrationView(CreateView):
    """A view to show/process the registration form to create a new User."""

    template_name = "blog/register.html"
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        """The URL to redirect to after creating a new User."""
        return reverse("login")


########################################################

## enable REST API for this application
from rest_framework import generics
from .serializers import *


# expose Article model as a list rather than single
class ArticleListAPIView(generics.ListCreateAPIView):
    """
    View will expose API for Articles with List and Create.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
