# File: mini_insta/views.py
# Author: Louise Lee, llouise@bu.edu, 09/25/2025
# Description: Defines view function, handles rendering of the different pages by using
# context data

from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
)  # look at all instances of model (detail = single instance)
from .models import Profile, Post, Photo
from .forms import CreatePostForm
from django.urls import reverse


# Create your views here.
class ProfileListView(ListView):
    """Define a view class to show all profiles."""

    # model name and template you want to use
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    # variable within html page, contain many profile instances
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """Display a single profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"


class PostDetailView(DetailView):
    """Display a single post"""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"


class CreatePostView(CreateView):
    """Handle creation of new post"""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    # Provide profile in context so the template can show @username and
    # build a URL that includes profile.pk
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(Profile, pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        """
        Method handles form submission, save new object to Django db.
        We need to add the foreign key (of Profile) to Post, then create the Photo
        """
        pk = self.kwargs["pk"]
        form.instance.profile = Profile.objects.get(pk=pk)

        response = super().form_valid(form)

        # Create the first Photo from the extra form field
        image_url = form.cleaned_data.get("image_url")
        if not image_url:  # empty -> fallback
            image_url = "https://media.istockphoto.com/id/1472933890/vector/no-image-vector-symbol-missing-available-icon-no-gallery-for-this-moment-placeholder.jpg?s=612x612&w=0&k=20&c=Rdn-lecwAj8ciQEccm0Ep2RX50FCuUJOaEM8qQjiLL0="

        Photo.objects.create(post=self.object, image_url=image_url)
        return response

    def get_success_url(self):
        """Provide URL to redirect to after create new post"""
        # create and return URL
        # return reverse("show_all")
        pk = self.kwargs["pk"]
        return reverse("show_profile", kwargs={"pk": pk})
