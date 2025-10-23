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
from django.contrib.auth.mixins import LoginRequiredMixin  # for authentication
from django.contrib.auth.forms import UserCreationForm  # for new User
from django.contrib.auth.models import User  # Django user model


# Create your views here.
class ProfileListView(ListView):
    """Define a view class to show all profiles."""

    # model name and template you want to use
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    # variable within html page, contain many profile instances
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        """Override the dispatch method to add debugging information."""

        if request.user.is_authenticated:
            print(f"ProfileListView.dispatch(): request.user={request.user}")
        else:
            print(f"ProfileListView.dispatch(): not logged in.")

        return super().dispatch(request, *args, **kwargs)


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


class CreatePostView(LoginRequiredMixin, CreateView):
    """Handle creation of new post"""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_login_url(self):
        """Return the URL for this app's login page"""
        return reverse("login")

    # Provide profile in context so the template can show @username and
    # build a URL that includes profile.pk
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)
        ctx["profile"] = profile
        return ctx

    def form_valid(self, form):
        """
        Method handles form submission, save new object to Django db.
        We need to add the foreign key (of Profile) to Post, then create the Photo
        """
        pk = self.kwargs["pk"]
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.profile = profile

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
        pk = self.object.profile.pk
        return reverse("show_profile", kwargs={"pk": pk})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """View class to handle update of post based on PK"""

    model = Profile
    template_name = "mini_insta/update_profile_form.html"
    form_class = UpdateProfileForm
    context_object_name = "profile"

    def get_login_url(self):
        return reverse("login")

    def get_object(self):
        # Profile for the logged-in user
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        # Redirect back to the updated profile page
        return self.object.get_absolute_url()


class DeletePostView(DeleteView):
    """Handle deletion of a Post"""

    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_login_url(self):
        return reverse("login")

    def get_queryset(self):
        # Only allow deleting your own posts
        return Post.objects.filter(profile__user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.object.profile
        return ctx

    def get_success_url(self):
        pk = self.object.profile.pk
        return reverse("show_profile", kwargs={"pk": pk})


class UpdatePostView(UpdateView):
    """Handle updating the caption of an existing post"""

    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/update_post_form.html"
    context_object_name = "post"

    def get_login_url(self):
        return reverse("login")

    def get_queryset(self):
        # Only allow updating your own posts
        return Post.objects.filter(profile__user=self.request.user)

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

    def get_login_url(self):
        return reverse("login")

    def get_queryset(self):
        self.profile = get_object_or_404(Profile, user=self.request.user)
        return self.profile.get_post_feed()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.profile
        return ctx


class SearchView(ListView):
    """Find query in and display search results"""

    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def get_login_url(self):
        return reverse("login")

    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, self.request.user)
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
