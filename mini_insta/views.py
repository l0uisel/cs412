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
    TemplateView,
    View,
)
from .models import Profile, Post, Photo, Follow, Like
from .forms import CreatePostForm, UpdateProfileForm, CreateProfileForm
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.
class ProfileListView(ListView):
    """Define a view class to show all profiles."""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
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

    def get_context_data(self, **kwargs):
        """Add additional context data"""
        ctx = super().get_context_data(**kwargs)

        # Check if the logged-in user is viewing their own profile
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.filter(user=self.request.user).first()
            ctx["user_profile"] = user_profile

            # Check if logged-in user follows this profile
            if user_profile and user_profile != self.object:
                ctx["is_following"] = Follow.objects.filter(
                    follower=user_profile, followed=self.object
                ).exists()
            else:
                ctx["is_following"] = False

        return ctx


class PostDetailView(DetailView):
    """Display a single post"""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """Add additional context data"""
        ctx = super().get_context_data(**kwargs)

        # Check if the logged-in user has liked this post
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.filter(user=self.request.user).first()
            ctx["user_profile"] = user_profile

            if user_profile:
                ctx["has_liked"] = Like.objects.filter(
                    profile=user_profile, post=self.object
                ).exists()
            else:
                ctx["has_liked"] = False

        return ctx


class CreatePostView(LoginRequiredMixin, CreateView):
    """Handle creation of new post"""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_login_url(self):
        """Return the URL for this app's login page"""
        return reverse("login")

    def get_context_data(self, **kwargs):
        """Provide profile in context so the template can show @username"""
        ctx = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)
        ctx["profile"] = profile
        return ctx

    def form_valid(self, form):
        """
        Method handles form submission, save new object to Django db.
        We need to add the foreign key (of Profile) to Post, then create the Photo
        """
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
        pk = self.object.profile.pk
        return reverse("show_profile", kwargs={"pk": pk})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """View class to handle update of post based on PK"""

    model = Profile
    template_name = "mini_insta/update_profile_form.html"
    form_class = UpdateProfileForm
    context_object_name = "profile"

    def get_login_url(self):
        """Return the URL for this app's login page"""
        return reverse("login")

    def get_object(self):
        """Profile for the logged-in user"""
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        """Redirect back to the updated profile page"""
        return self.object.get_absolute_url()


class DeletePostView(LoginRequiredMixin, DeleteView):
    """Handle deletion of a Post"""

    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_login_url(self):
        """Return the URL for this app's login page"""
        return reverse("login")

    def get_queryset(self):
        """Only allow deleting your own posts"""
        return Post.objects.filter(profile__user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.object.profile
        return ctx

    def get_success_url(self):
        pk = self.object.profile.pk
        return reverse("show_profile", kwargs={"pk": pk})


class UpdatePostView(LoginRequiredMixin, UpdateView):
    """Handle updating the caption of an existing post"""

    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/update_post_form.html"
    context_object_name = "post"

    def get_login_url(self):
        """Return the URL for this app's login page"""
        return reverse("login")

    def get_queryset(self):
        """Only allow updating your own posts"""
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


class PostFeedListView(LoginRequiredMixin, ListView):
    """Display profile's feed"""

    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_login_url(self):
        """Return the URL for this app's login page"""
        return reverse("login")

    def get_queryset(self):
        self.profile = get_object_or_404(Profile, user=self.request.user)
        return self.profile.get_post_feed()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.profile
        return ctx


class SearchView(LoginRequiredMixin, ListView):
    """Find query in and display search results"""

    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def get_login_url(self):
        """Return the URL for this app's login page"""
        return reverse("login")

    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, user=self.request.user)
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


class CreateProfileView(CreateView):
    """Register user and create a linked profile in one submit"""

    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # If we already tried to validate user_form, reuse it (so errors show). Otherwise, blank.
        ctx.setdefault("user_form", UserCreationForm())
        return ctx

    def form_valid(self, form):
        """Handle both UserCreationForm and CreateProfileForm"""
        # Build the user form from POST and validate it too
        user_form = UserCreationForm(self.request.POST)
        if not user_form.is_valid():
            # Re-render the page with errors from both forms
            ctx = self.get_context_data(form=form)
            ctx["user_form"] = user_form
            return self.render_to_response(ctx)

        # Create user
        user = user_form.save()

        # Log user in
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")

        # Attach user to the new Profile before saving the Profile
        form.instance.user = user

        # Save Profile via the normal CreateView path
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        """Made account, send them to their new profile page"""
        return reverse("show_profile", kwargs={"pk": self.object.pk})


def _redirect_back(request, fallback_url_name, **fallback_kwargs):
    """Send the user back to HTTP_REFERER; otherwise to a reasonable page."""
    ref = request.META.get("HTTP_REFERER")
    if ref:
        return redirect(ref)
    return redirect(
        reverse(fallback_url_name, kwargs=fallback_kwargs)
        if fallback_kwargs
        else reverse(fallback_url_name)
    )


class FollowProfileView(LoginRequiredMixin, View):
    """Follow another profile"""

    def get_login_url(self):
        """Return the URL for this app's login page"""
        return reverse("login")

    def post(self, request, pk):
        """Handle follow action"""
        me = Profile.objects.filter(user=request.user).first()
        other = Profile.objects.filter(pk=pk).first()
        if not me or not other:
            messages.error(request, "Profile not found.")
            return _redirect_back(request, "show_all_profiles")

        if me.pk == other.pk:
            messages.warning(request, "You can't follow yourself.")
            return _redirect_back(request, "show_profile", pk=other.pk)

        Follow.objects.get_or_create(follower=me, followed=other)
        messages.success(request, f"You're now following @{other.username}.")
        return _redirect_back(request, "show_profile", pk=other.pk)


class UnfollowProfileView(LoginRequiredMixin, View):
    """Unfollow another profile"""

    def get_login_url(self):
        """Return the URL for this app's login page"""
        return reverse("login")

    def post(self, request, pk):
        """Handle unfollow action"""
        me = Profile.objects.filter(user=request.user).first()
        other = Profile.objects.filter(pk=pk).first()
        if not me or not other:
            messages.error(request, "Profile not found.")
            return _redirect_back(request, "show_all_profiles")

        Follow.objects.filter(follower=me, followed=other).delete()
        messages.info(request, f"Unfollowed @{other.username}.")
        return _redirect_back(request, "show_profile", pk=other.pk)


class LikePostView(LoginRequiredMixin, View):
    """Like a post (cannot like your own)"""

    def get_login_url(self):
        """Return the URL for this app's login page"""
        return reverse("login")

    def post(self, request, pk):
        """Handle like action"""
        me = Profile.objects.filter(user=request.user).first()
        post = Post.objects.filter(pk=pk).select_related("profile").first()
        if not me or not post:
            messages.error(request, "Post not found.")
            return _redirect_back(request, "show_all_profiles")

        if post.profile_id == me.pk:
            messages.warning(request, "You can't like your own post.")
            return _redirect_back(request, "show_post", pk=post.pk)

        Like.objects.get_or_create(profile=me, post=post)
        messages.success(request, "Liked the post.")
        return _redirect_back(request, "show_post", pk=post.pk)


class UnlikePostView(LoginRequiredMixin, View):
    """Remove like"""

    def get_login_url(self):
        """Return the URL for this app's login page"""
        return reverse("login")

    def post(self, request, pk):
        """Handle unlike action"""
        me = Profile.objects.filter(user=request.user).first()
        post = Post.objects.filter(pk=pk).first()
        if not me or not post:
            messages.error(request, "Post not found.")
            return _redirect_back(request, "show_all_profiles")

        Like.objects.filter(profile=me, post=post).delete()
        messages.info(request, "Removed like.")
        return _redirect_back(request, "show_post", pk=post.pk)
