# File: mini_insta/views.py
# Author: Louise Lee, llouise@bu.edu, 09/25/2025
# Description: Defines view function, handles rendering of the different pages by using
# context data

from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)  # look at all instances of model (detail = single instance)
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm
from django.urls import reverse
from django.db.models import Q


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

        # Pull multiple uploaded files from <input name="files" multiple>
        files = self.request.FILES.getlist("files")

        # Create a Photo for each uploaded file
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        if not files:
            Photo.objects.create(
                post=self.object,
                image_url="https://media.istockphoto.com/id/1472933890/vector/no-image-vector-symbol-missing-available-icon-no-gallery-for-this-moment-placeholder.jpg?s=612x612&w=0&k=20&c=Rdn-lecwAj8ciQEccm0Ep2RX50FCuUJOaEM8qQjiLL0=",
            )

        return response

    def get_success_url(self):
        """Provide URL to redirect to after create new post"""
        # create and return URL
        # return reverse("show_all")
        pk = self.kwargs["pk"]
        return reverse("show_profile", kwargs={"pk": pk})


class UpdateProfileView(UpdateView):
    """View class to handle update of post based on PK"""

    model = Profile
    template_name = "mini_insta/update_profile_form.html"
    form_class = UpdateProfileForm
    context_object_name = "profile"

    def get_success_url(self):
        # Redirect back to the updated profile page
        return self.object.get_absolute_url()


class DeletePostView(DeleteView):
    """Handle deletion of a Post"""

    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["profile"] = post.profile
        return context

    def get_success_url(self):
        """Redirect to the profile page after successful delete"""
        post = self.get_object()
        pk = post.profile.pk
        return reverse("show_profile", kwargs={"pk": pk})


class UpdatePostView(UpdateView):
    """Handle updating the caption of an existing post"""

    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/update_post_form.html"
    context_object_name = "post"

    def get_success_url(self):
        """Redirect to the post page after update"""
        pk = self.object.pk
        return reverse("show_post", kwargs={"pk": pk})


class ShowFollowersDetailView(DetailView):
    """Display followers of profile"""

    model = Profile
    template_name = "mini_insta/show_followers.html"


class ShowFollowingDetailView(DetailView):
    """Display a profile's following"""

    model = Profile
    template_name = "mini_insta/show_following.html"


class PostFeedListView(ListView):
    """Display profile's feed"""

    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        self.profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        return self.profile.get_post_feed()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.profile
        return ctx


class SearchView(ListView):
    """Find query in and display search results"""

    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        self.query = request.GET.get("q", "").strip()
        if not self.query:
            return render(request, "mini_insta/search.html", {"profile": self.profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if not self.query:
            return Post.objects.none()
        return (
            Post.objects.filter(caption__icontains=self.query)
            .select_related("profile")
            .order_by("-timestamp")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.profile
        ctx["query"] = self.query
        ctx["profiles"] = Profile.objects.filter(
            Q(username__icontains=self.query)
            | Q(display_name__icontains=self.query)
            | Q(bio_text__icontains=self.query)
        ).order_by("username")
        return ctx
